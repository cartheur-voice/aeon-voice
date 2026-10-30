#!/usr/bin/env python3
"""Validate a consented PCM WAV corpus before AeonVoice HTS import."""

import argparse
import json
import math
import sys
import wave
from pathlib import Path


def read_metadata(path):
    entries = {}
    problems = []
    for number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if "|" not in line:
            problems.append(f"metadata line {number}: expected id|transcript")
            continue
        clip_id, transcript = (part.strip() for part in line.split("|", 1))
        if not clip_id or not transcript:
            problems.append(f"metadata line {number}: ID and transcript are required")
        elif clip_id in entries:
            problems.append(f"metadata line {number}: duplicate ID {clip_id}")
        else:
            entries[clip_id] = transcript
    return entries, problems


def edge_silence(samples, threshold):
    active = [abs(sample) >= threshold for sample in samples]
    if not any(active):
        return None, None
    first = next(index for index, value in enumerate(active) if value)
    last = len(active) - next(index for index, value in enumerate(reversed(active)) if value)
    return first, len(active) - last


def inspect_wav(path, sample_rate, max_edge_silence_ms):
    result = {"file": str(path)}
    try:
        with wave.open(str(path), "rb") as audio:
            channels = audio.getnchannels()
            width = audio.getsampwidth()
            rate = audio.getframerate()
            frames = audio.getnframes()
            compression = audio.getcomptype()
            raw = audio.readframes(frames)
    except (wave.Error, OSError) as error:
        result["error"] = f"cannot read WAV: {error}"
        return result
    result.update({"channels": channels, "sample_rate": rate, "sample_width_bits": width * 8,
                   "duration_seconds": round(frames / rate, 3) if rate else 0})
    failures = []
    warnings = []
    if compression != "NONE" or width != 2 or channels != 1 or rate != sample_rate:
        failures.append("expected uncompressed 16-bit PCM, mono, %d Hz" % sample_rate)
    if frames == 0:
        failures.append("empty recording")
    if width == 2 and channels == 1 and frames:
        samples = [int.from_bytes(raw[i:i + 2], "little", signed=True) for i in range(0, len(raw), 2)]
        peak = max(abs(sample) for sample in samples)
        result["peak_dbfs"] = round(20 * math.log10(peak / 32768), 2) if peak else None
        start, end = edge_silence(samples, 327)
        if start is None:
            failures.append("silent recording")
        else:
            result["leading_silence_ms"] = round(start * 1000 / rate)
            result["trailing_silence_ms"] = round(end * 1000 / rate)
            if peak >= 32760:
                warnings.append("peak is at or near digital clipping")
            if start * 1000 / rate > max_edge_silence_ms:
                warnings.append("leading silence exceeds %d ms" % max_edge_silence_ms)
            if end * 1000 / rate > max_edge_silence_ms:
                warnings.append("trailing silence exceeds %d ms" % max_edge_silence_ms)
    result["failures"] = failures
    result["warnings"] = warnings
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--wav-dir", required=True, type=Path)
    parser.add_argument("--metadata", required=True, type=Path)
    parser.add_argument("--evaluation-ids", type=Path)
    parser.add_argument("--report", type=Path)
    parser.add_argument("--sample-rate", type=int, default=24000)
    parser.add_argument("--max-edge-silence-ms", type=int, default=1000)
    parser.add_argument("--recursive", action="store_true",
                        help="search for WAV files in batch subdirectories")
    parser.add_argument("--exclude-id", action="append", default=[],
                        help="WAV stem to deliberately omit, for example a discarded retake")
    args = parser.parse_args()
    entries, errors = read_metadata(args.metadata)
    wave_paths = args.wav_dir.rglob("*.wav") if args.recursive else args.wav_dir.glob("*.wav")
    wavs = {}
    for file in wave_paths:
        if file.stem in wavs:
            errors.append("duplicate recording ID: %s" % file.stem)
        else:
            wavs[file.stem] = file
    excluded = set(args.exclude_id)
    unexpected_exclusions = sorted(excluded - set(wavs))
    errors.extend("excluded recording does not exist: %s.wav" % item
                  for item in unexpected_exclusions)
    wavs = {clip_id: path for clip_id, path in wavs.items() if clip_id not in excluded}
    if not entries:
        errors.append("no metadata entries found")
    missing = sorted(set(entries) - set(wavs))
    extra = sorted(set(wavs) - set(entries))
    errors.extend("missing recording: %s.wav" % item for item in missing)
    errors.extend("recording has no transcript: %s.wav" % item for item in extra)
    evaluation_ids = set()
    if args.evaluation_ids and args.evaluation_ids.exists():
        evaluation_ids = {line.strip() for line in args.evaluation_ids.read_text().splitlines()
                          if line.strip() and not line.startswith("#")}
        unknown = sorted(evaluation_ids - set(entries))
        errors.extend("evaluation ID has no transcript: %s" % item for item in unknown)
    files = [inspect_wav(wavs[clip_id], args.sample_rate, args.max_edge_silence_ms)
             for clip_id in sorted(set(entries) & set(wavs))]
    errors.extend("%s: %s" % (Path(item["file"]).name, failure)
                  for item in files for failure in item.get("failures", []))
    report = {"metadata_entries": len(entries), "wav_files": len(wavs),
              "excluded_recordings": sorted(excluded),
              "evaluation_entries": len(evaluation_ids), "errors": errors,
              "warnings": ["%s: %s" % (Path(item["file"]).name, warning)
                           for item in files for warning in item.get("warnings", [])],
              "files": files}
    rendered = json.dumps(report, indent=2) + "\n"
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    if errors:
        print("Corpus QA failed with %d error(s)." % len(errors), file=sys.stderr)
        return 1
    print("Corpus QA passed: %d recordings (%d evaluation IDs); %d warning(s)." %
          (len(files), len(evaluation_ids), len(report["warnings"])))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
