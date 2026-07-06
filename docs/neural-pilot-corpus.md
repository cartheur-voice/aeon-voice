# Neural Pilot Corpus

## Purpose

This note records the current experimental corpus being used to validate the neural voice prep flow.

It is a **pipeline/prototyping source**, not a final statement about Leena's eventual neural voice identity.

## Current Source

- dataset family: Libre English Hi-Fi TTS
- selected subset: `6097_clean/13657`
- extracted local source: `work/leena-neural-source/hi_fi_tts_v0/`

## Why We Are Using It

- it gives us a reproducible single-speaker slice
- it is already extracted locally
- it lets us exercise the export, transcript, and eval workflow now

## Known Limitation

This source is being used because it is available and workable for the experiment flow.
It should be considered swappable.

## Extracted Source Shape

The local extracted source contains:

- `audio/6097_clean/13657/`
- `6097_manifest_clean_train.13657.json`
- `6097_manifest_clean_dev.13657.json`
- `6097_manifest_clean_test.13657.json`
- the original clean manifests
- `LICENSE.txt`
- `readers_books_clean.txt`

## Pilot Export

The current pilot workspace is:

- `work/leena-neural-pilot/`

It was produced with:

```bash
python3 scripts/prepare-libre-english-subset.py \
  --dataset-dir work/leena-neural-source/hi_fi_tts_v0 \
  --manifest 6097_manifest_clean_train.13657.json \
  export-subset \
  --subset 6097_clean/13657 \
  --output-dir work/leena-neural-pilot \
  --max-clips 500 \
  --eval-count 25 \
  --eval-stride 20 \
  --sample-rate 24000 \
  --min-duration 1.0 \
  --max-duration 12.0 \
  --transcript-field text_normalized
```

## Current Pilot Contents

- `500` WAV files
- `475` train clips
- `25` eval clips
- `text.csv`
- `metadata.csv`
- `train.ssml`
- `eval.ssml`
- `selection.json`

## Next Use

This pilot corpus is suitable for:

- quick waveform/transcript QA
- first training experiments
- backend and tooling integration
- replacing later with a better-matched source while keeping the same workflow

## Chosen Stack For This Pilot

The current pilot is intended to feed the first `Piper` training experiments.

That is mainly because the pilot corpus already matches Piper's expected single-speaker `wav/` plus metadata workflow closely enough to keep branch momentum high.
