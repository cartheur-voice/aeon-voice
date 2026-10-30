# Male Natural: custom-voice starter

This is a development kit for a new, consented human voice.  It is **not** a
runtime voice yet: a new AeonVoice timbre requires a trained HTS model, which
is intentionally not derived from an existing bundled voice.

## Voice brief

| Field | Initial target |
| --- | --- |
| Voice ID | `male-natural` (working name; change before packaging) |
| Language | English |
| Character | Present, warm, conversational narrator |
| Delivery | Measured pace, clear consonants, comfortable short pauses |
| Recording format | Mono, 16-bit PCM WAV, 24 kHz |
| Corpus goal | 1,500 recorded lines; hold out 100 evaluation lines |

Do not record or train until the performer has signed the applicable voice,
likeness, and training-data consent.  Keep the signed consent and session
notes outside this repository unless they are explicitly approved for source
control.

## Record a corpus

Put recordings in `corpus/wav/` and add one line per recording to
`corpus/metadata.psv`:

```text
000001|I am here with you.
000002|Let us take this one step at a time.
```

The filename stem must exactly match the first field.  Record each line once,
in the same room, with the same microphone position and gain.  Preserve
natural delivery; do not add noise reduction, reverb, or aggressive dynamics
processing.  Leave roughly 150–300 ms of room tone at either end.

`prompts/seed.psv` is a short starting set for the intended delivery.  Expand
it into a balanced 1,500-line script before recording: include questions,
brief replies, numbers, dates, names, corrections, gentle reassurance, and
longer narration.  Move only the prompts actually recorded into
`metadata.psv`; that manifest is the corpus source of truth.

Use the planned evaluation IDs in `corpus/evaluation-ids.txt`; never include
those recordings in training.

## Check before importing

Run this from the repository root after adding recordings:

```bash
python3 voices/custom/male-natural/tools/validate_corpus.py \
  --wav-dir voices/custom/male-natural/corpus/wav \
  --metadata voices/custom/male-natural/corpus/metadata.psv \
  --evaluation-ids voices/custom/male-natural/corpus/evaluation-ids.txt \
  --report /tmp/male-natural-corpus-report.json
```

It rejects missing or extra IDs and reports files that are not 24 kHz, mono,
16-bit PCM WAV, are silent, clip, or have unusually long edge silence.  Fix
errors before training; review warnings with headphones.  This is a technical
quality check, not proof of consent or of transcript accuracy.

## Train when the corpus passes QA

1. Build the development helpers: `scons dev=True -j4`.
2. Copy `training.cfg.example.json` into an empty training workspace as
   `training.cfg`, then replace every `REPLACE_WITH_...` value with an absolute
   path.  Do not edit the repository-wide `src/scripts/general/training.cfg`.
3. Initialize the HTS scaffold and follow [the custom voice guide](../../../doc/CustomVoice.md).
4. Package the exported model as `data/voices/<final-voice-id>/`, incrementing
   `revision` for each trained model.
5. Listen to the fixed evaluation set before accepting the model; compare it
   against the same reference takes, not just training phrases.

Raw recordings, generated reports, and training workspaces are deliberately
ignored by Git.  Only scripts, prompts, manifests, and approved reference
samples should be committed.
