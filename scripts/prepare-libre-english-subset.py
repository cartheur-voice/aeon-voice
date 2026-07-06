#!/usr/bin/env python3

import argparse
import csv
import json
import os
import shutil
import subprocess
import sys
import tarfile
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


DEFAULT_TAR = "/home/cartheur/downloads/libre-english/hi_fi_tts_v0.tar.gz"
DEFAULT_DATASET_DIR = "work/libre-english-unpacked/hi_fi_tts_v0"
DEFAULT_MANIFEST = "hi_fi_tts_v0/6097_manifest_clean_train.json"


@dataclass
class Entry:
    source_audio_path: str
    speaker_group: str
    speaker_id: str
    clip_name: str
    duration: float
    text: str
    text_normalized: str
    text_no_preprocessing: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Inspect or export a single-speaker Libre English subset for AeonVoice experiments."
    )
    parser.add_argument("--tar-path", default=DEFAULT_TAR, help="Path to hi_fi_tts_v0.tar.gz")
    parser.add_argument(
        "--dataset-dir",
        default=None,
        help="Path to an unpacked hi_fi_tts_v0 directory. Faster than reading from the tarball.",
    )
    parser.add_argument(
        "--manifest",
        default=DEFAULT_MANIFEST,
        help="Manifest path relative to the dataset root or member path inside the tarball",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    list_parser = subparsers.add_parser("list-subsets", help="Summarize available speaker subsets")
    list_parser.add_argument("--limit", type=int, default=20, help="Maximum number of subsets to print")

    export_parser = subparsers.add_parser("export-subset", help="Export one subset to a workspace")
    export_parser.add_argument(
        "--subset",
        required=True,
        help="Subset in speaker_group/speaker_id form, for example 6097_clean/14411",
    )
    export_parser.add_argument("--output-dir", required=True, help="Directory to create")
    export_parser.add_argument("--max-clips", type=int, default=800, help="Maximum clips to export")
    export_parser.add_argument("--eval-count", type=int, default=50, help="Held-out evaluation clip count")
    export_parser.add_argument(
        "--eval-stride",
        type=int,
        default=20,
        help="Take every Nth selected clip into eval until eval-count is reached",
    )
    export_parser.add_argument("--sample-rate", type=int, default=24000, help="Target WAV sample rate")
    export_parser.add_argument("--min-duration", type=float, default=1.0, help="Minimum clip duration in seconds")
    export_parser.add_argument("--max-duration", type=float, default=12.0, help="Maximum clip duration in seconds")
    export_parser.add_argument(
        "--transcript-field",
        choices=["text_normalized", "text_no_preprocessing", "text"],
        default="text_normalized",
        help="Transcript field to write into the exported corpus",
    )

    return parser.parse_args()


def normalize_manifest_path(manifest_path: str) -> str:
    manifest = Path(manifest_path)
    if manifest.parts and manifest.parts[0] == "hi_fi_tts_v0":
        manifest = Path(*manifest.parts[1:])
    return manifest.as_posix()


def resolve_dataset_root(args: argparse.Namespace) -> Path | None:
    if not args.dataset_dir:
        return None
    root = Path(args.dataset_dir)
    if (root / "audio").is_dir():
        return root
    candidate = root / "hi_fi_tts_v0"
    if (candidate / "audio").is_dir():
        return candidate
    raise FileNotFoundError(f"No hi_fi_tts_v0 dataset root found under {args.dataset_dir}")


def iter_manifest_entries_from_tar(tar_path: str, manifest_member: str) -> Iterable[Entry]:
    with tarfile.open(tar_path, "r:gz") as archive:
        manifest_file = archive.extractfile(manifest_member)
        if manifest_file is None:
            raise FileNotFoundError(f"Manifest {manifest_member} was not found in {tar_path}")

        for raw_line in manifest_file:
            line = raw_line.decode("utf-8").strip()
            if not line:
                continue
            payload = json.loads(line)
            audio_path = payload["audio_filepath"]
            parts = audio_path.split("/")
            if len(parts) < 3:
                continue
            speaker_group = parts[1]
            speaker_id = parts[2]
            yield Entry(
                source_audio_path=f"hi_fi_tts_v0/{audio_path}",
                speaker_group=speaker_group,
                speaker_id=speaker_id,
                clip_name=Path(parts[-1]).stem,
                duration=float(payload.get("duration", 0.0)),
                text=payload.get("text", "").strip(),
                text_normalized=payload.get("text_normalized", "").strip(),
                text_no_preprocessing=payload.get("text_no_preprocessing", "").strip(),
            )


def iter_manifest_entries_from_dir(dataset_root: Path, manifest_path: str) -> Iterable[Entry]:
    manifest_file = dataset_root / normalize_manifest_path(manifest_path)
    if not manifest_file.is_file():
        raise FileNotFoundError(f"Manifest {manifest_file} was not found")

    with manifest_file.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            payload = json.loads(line)
            audio_path = payload["audio_filepath"]
            parts = audio_path.split("/")
            if len(parts) < 3:
                continue
            speaker_group = parts[1]
            speaker_id = parts[2]
            yield Entry(
                source_audio_path=(dataset_root / audio_path).as_posix(),
                speaker_group=speaker_group,
                speaker_id=speaker_id,
                clip_name=Path(parts[-1]).stem,
                duration=float(payload.get("duration", 0.0)),
                text=payload.get("text", "").strip(),
                text_normalized=payload.get("text_normalized", "").strip(),
                text_no_preprocessing=payload.get("text_no_preprocessing", "").strip(),
            )


def iter_manifest_entries(args: argparse.Namespace) -> Iterable[Entry]:
    dataset_root = resolve_dataset_root(args)
    if dataset_root is not None:
        return iter_manifest_entries_from_dir(dataset_root, args.manifest)
    return iter_manifest_entries_from_tar(args.tar_path, args.manifest)


def transcript_for(entry: Entry, field_name: str) -> str:
    value = getattr(entry, field_name)
    if value:
        return value
    for fallback in (entry.text_normalized, entry.text_no_preprocessing, entry.text):
        if fallback:
            return fallback
    return ""


def require_command(name: str) -> None:
    if shutil.which(name) is None:
        raise RuntimeError(f"Required command not found in PATH: {name}")


def summarize_subsets(entries: Iterable[Entry]) -> list[tuple[str, int, float]]:
    totals: dict[str, tuple[int, float]] = {}
    for entry in entries:
        key = f"{entry.speaker_group}/{entry.speaker_id}"
        count, seconds = totals.get(key, (0, 0.0))
        totals[key] = (count + 1, seconds + entry.duration)
    ordered = sorted(totals.items(), key=lambda item: (-item[1][1], -item[1][0], item[0]))
    return [(key, count, seconds) for key, (count, seconds) in ordered]


def format_hours(seconds: float) -> str:
    return f"{seconds / 3600.0:.2f}h"


def make_ssml(entries: list[tuple[str, str]]) -> str:
    lines = ['<?xml version="1.0" encoding="UTF-8"?>', "<speak>"]
    for clip_id, text in entries:
        escaped = (
            text.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
        )
        lines.append(f'  <s xml:id="{clip_id}">{escaped}</s>')
    lines.append("</speak>")
    return "\n".join(lines) + "\n"


def export_subset(args: argparse.Namespace) -> int:
    require_command("ffmpeg")
    dataset_root = resolve_dataset_root(args)

    selected: list[Entry] = []
    subset_key = args.subset
    for entry in iter_manifest_entries(args):
        key = f"{entry.speaker_group}/{entry.speaker_id}"
        if key != subset_key:
            continue
        if entry.duration < args.min_duration or entry.duration > args.max_duration:
            continue
        if not transcript_for(entry, args.transcript_field):
            continue
        selected.append(entry)
        if len(selected) >= args.max_clips:
            break

    if not selected:
        print(f"No matching clips found for subset {subset_key}", file=sys.stderr)
        return 1

    output_dir = Path(args.output_dir)
    wav_dir = output_dir / "wav"
    wav_dir.mkdir(parents=True, exist_ok=True)

    metadata_path = output_dir / "metadata.csv"
    text_csv_path = output_dir / "text.csv"
    train_ssml_path = output_dir / "train.ssml"
    eval_ssml_path = output_dir / "eval.ssml"
    selection_path = output_dir / "selection.json"

    train_entries: list[tuple[str, str]] = []
    eval_entries: list[tuple[str, str]] = []

    jobs = []
    for index, entry in enumerate(selected, start=1):
        clip_id = f"{index:06d}"
        jobs.append(
            {
                "clip_id": clip_id,
                "entry": entry,
                "transcript": transcript_for(entry, args.transcript_field),
                "wav_path": wav_dir / f"{clip_id}.wav",
            }
        )

    with metadata_path.open("w", encoding="utf-8", newline="") as metadata_file, \
            text_csv_path.open("w", encoding="utf-8", newline="") as text_csv_file:
        metadata_writer = csv.writer(metadata_file)
        metadata_writer.writerow(
            ["clip_id", "subset", "source_audio", "duration_seconds", "transcript_field", "transcript"]
        )

        for job in jobs:
            clip_id = job["clip_id"]
            entry = job["entry"]
            transcript = job["transcript"]
            source_path = entry.source_audio_path
            job["wav_path"].parent.mkdir(parents=True, exist_ok=True)

            if dataset_root is None:
                with tarfile.open(args.tar_path, "r:gz") as archive:
                    member = archive.extractfile(source_path)
                    if member is None:
                        raise FileNotFoundError(f"Audio member {source_path} was not found in the tarball")

                    with tempfile.NamedTemporaryFile(suffix=".flac", delete=False) as temp_audio:
                        temp_audio.write(member.read())
                        temp_audio_path = temp_audio.name

                try:
                    subprocess.run(
                        [
                            "ffmpeg",
                            "-nostdin",
                            "-loglevel",
                            "error",
                            "-y",
                            "-i",
                            temp_audio_path,
                            "-ac",
                            "1",
                            "-ar",
                            str(args.sample_rate),
                            str(job["wav_path"]),
                        ],
                        check=True,
                    )
                finally:
                    os.unlink(temp_audio_path)
            else:
                if not os.path.isfile(source_path):
                    raise FileNotFoundError(f"Audio file {source_path} was not found")
                subprocess.run(
                    [
                        "ffmpeg",
                        "-nostdin",
                        "-loglevel",
                        "error",
                        "-y",
                        "-i",
                        source_path,
                        "-ac",
                        "1",
                        "-ar",
                        str(args.sample_rate),
                        str(job["wav_path"]),
                    ],
                    check=True,
                )

            text_csv_file.write(f"{clip_id}|{transcript}\n")
            metadata_writer.writerow(
                [
                    clip_id,
                    subset_key,
                    source_path,
                    f"{entry.duration:.2f}",
                    args.transcript_field,
                    transcript,
                ]
            )

            destination = train_entries
            if len(eval_entries) < args.eval_count and ((int(clip_id) - 1) % args.eval_stride == 0):
                destination = eval_entries
            destination.append((clip_id, transcript))

    train_ssml_path.write_text(make_ssml(train_entries), encoding="utf-8")
    eval_ssml_path.write_text(make_ssml(eval_entries), encoding="utf-8")
    selection_path.write_text(
        json.dumps(
            {
                "dataset_dir": str(dataset_root) if dataset_root is not None else None,
                "tar_path": args.tar_path,
                "manifest": args.manifest,
                "subset": subset_key,
                "selected_clip_count": len(selected),
                "train_clip_count": len(train_entries),
                "eval_clip_count": len(eval_entries),
                "sample_rate": args.sample_rate,
                "min_duration": args.min_duration,
                "max_duration": args.max_duration,
                "transcript_field": args.transcript_field,
                "max_clips": args.max_clips,
                "eval_stride": args.eval_stride,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    print(f"Exported {len(selected)} clips from {subset_key} to {output_dir}")
    print(f"Train clips: {len(train_entries)}")
    print(f"Eval clips:  {len(eval_entries)}")
    print(f"Transcript field: {args.transcript_field}")
    return 0


def main() -> int:
    args = parse_args()

    if args.command == "list-subsets":
        summary = summarize_subsets(iter_manifest_entries(args))
        print("subset,count,total_duration")
        for key, count, seconds in summary[: args.limit]:
            print(f"{key},{count},{format_hours(seconds)}")
        return 0

    if args.command == "export-subset":
        return export_subset(args)

    raise ValueError(f"Unsupported command: {args.command}")


if __name__ == "__main__":
    raise SystemExit(main())
