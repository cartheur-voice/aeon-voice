# Leena Naturalness Plan

## Current state

Leena is an HTS-style packaged voice in:

- `data/voices/leena/16000/`
- `data/voices/leena/24000/`

The current repo already documents two separate levers:

1. Wrapper tuning via `AeonVoice.conf`
2. Rebuilding the compiled voice artifacts under `data/voices/leena/`

The existing Leena audition notes in `docs/voice-samples/leena/` indicate the easy wrapper-side tuning has already been explored. That means the remaining "more natural" work is likely model-side.

## What the Libre English download is

The dataset at `/home/cartheur/downloads/libre-english/hi_fi_tts_v0.tar.gz` looks like a multi-speaker audiobook-style corpus with:

- manifest JSON files
- FLAC audio
- normalized and original text
- train/dev/test splits

This is useful, but it does **not** match AeonVoice's training workflow directly. The repo's custom-voice flow in `doc/CustomVoice.md` expects a single-speaker corpus prepared roughly like:

- one speaker identity
- WAV files
- stable sample rate
- matching transcript IDs
- held-out eval set

## Best fit for this corpus

The Libre English corpus is a better fit for **bootstrapping or adapting a replacement Leena-like voice** than for trying to repair the current voice in place.

Most likely path:

1. Select one strong female speaker subset from the corpus.
2. Convert the selected clips from FLAC to mono WAV at `24000` Hz.
3. Build AeonVoice training text files from the manifest.
4. Train a new English female voice in the HTS workflow.
5. Compare the new package against current Leena with the existing audition scripts.

## Risks and constraints

- Multi-speaker data will reduce naturalness if mixed into one HTS voice.
- Audiobook narration can sound expressive, but may also create unstable style shifts across chapters.
- Short clips and inconsistent punctuation normalization can hurt prosody if not cleaned.
- This corpus may improve smoothness and coverage, but it will not make AeonVoice behave like a modern neural TTS stack.
- Licensing still needs to be checked before packaging any derived voice for distribution.

## Recommended next steps

### Low-risk

Use the corpus as a **candidate source** for a new experimental voice rather than overwriting `data/voices/leena/` first.

### Practical workflow

1. Unpack the tarball into a temporary working directory.
2. Pick one female speaker/book subset with enough duration and consistent tone.
3. Export a small pilot set, around 300-800 utterances.
4. Run the AeonVoice import and label pipeline from `src/scripts/general/voice-building-utils`.
5. Train a first-pass voice at `24000` Hz.
6. Render the same audition text used in `docs/voice-samples/leena/leena-midpoint.txt`.
7. Only if the pilot beats current Leena should we invest in a larger full-corpus preparation pass.

## Recommendation

If the goal is "make Leena sound more natural," the strongest next move is:

- do **not** merge multiple Libre English speakers into Leena
- do create a single-speaker experimental voice from one carefully chosen subset
- do compare it against Leena before deciding whether to replace or retune anything

If we want, the next implementation step can be a small prep script that extracts one chosen Libre English manifest subset into the WAV plus transcript layout expected by AeonVoice training.
