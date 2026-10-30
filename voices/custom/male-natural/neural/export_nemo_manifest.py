#!/usr/bin/env python3
"""Export an AeonVoice custom-voice corpus as train/evaluation NeMo JSONL."""

import argparse
import json
import wave
from pathlib import Path


def read_metadata(path):
    entries = {}
    for number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        try:
            clip_id, text = (value.strip() for value in line.split("|", 1))
        except ValueError as error:
            raise ValueError(f"{path}:{number}: expected id|transcript") from error
        if not clip_id or not text or clip_id in entries:
            raise ValueError(f"{path}:{number}: invalid or duplicate utterance ID")
        entries[clip_id] = text
    return entries


def read_ids(path):
    return {line.strip() for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.startswith("#")}


def duration_seconds(path):
    with wave.open(str(path), "rb") as audio:
        if audio.getnchannels() != 1 or audio.getsampwidth() != 2:
            raise ValueError(f"{path}: expected mono PCM16 WAV")
        return round(audio.getnframes() / audio.getframerate(), 3)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--audio-root", required=True, type=Path)
    parser.add_argument("--metadata", required=True, type=Path)
    parser.add_argument("--evaluation-ids", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--speaker", default="male-natural")
    parser.add_argument("--language", default="en")
    args = parser.parse_args()

    audio_root = args.audio_root.resolve()
    entries = read_metadata(args.metadata)
    evaluation_ids = read_ids(args.evaluation_ids)
    if not evaluation_ids <= entries.keys():
        raise ValueError("evaluation IDs must exist in metadata")
    clips = {}
    for wav in audio_root.rglob("*.wav"):
        if wav.stem in entries:
            if wav.stem in clips:
                raise ValueError(f"duplicate audio for ID {wav.stem}")
            clips[wav.stem] = wav
    missing = sorted(set(entries) - set(clips))
    if missing:
        raise ValueError("missing audio: " + ", ".join(missing))

    manifests = {"train": [], "evaluation": []}
    for clip_id in sorted(entries):
        wav = clips[clip_id]
        item = {
            "audio_filepath": str(wav.relative_to(audio_root)),
            "text": entries[clip_id],
            "duration": duration_seconds(wav),
            "speaker": args.speaker,
            "language": args.language,
        }
        split = "evaluation" if clip_id in evaluation_ids else "train"
        manifests[split].append(item)

    args.output_dir.mkdir(parents=True, exist_ok=True)
    for split, rows in manifests.items():
        destination = args.output_dir / f"{split}.jsonl"
        destination.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows),
                               encoding="utf-8")
        print(f"{destination}: {len(rows)} utterances")


if __name__ == "__main__":
    main()
