# Creating A Custom Voice

This guide is for creating a **new trained voice** (not only tuning `-r/-t/-v`).

## Scope

This repo contains runtime synthesis and integration tools, but not a full end-to-end trainer.
Typical workflow:

1. Record and prepare a high-quality dataset.
2. Train HTS-compatible models in an external training pipeline.
3. Package the trained model into `data/voices/<voice_id>/`.
4. Validate with `AeonVoice-test`.

## 1. Define The Voice Target

Before recording, define:

- Character name and role (example: "Henry, emotional toy bear")
- Target language (`English`, `Russian`, etc.)
- Tone keywords (example: `warm`, `gentle`, `reassuring`)
- Delivery constraints (slow pace, short sentence cadence, etc.)

Create a script set:

- 1200-3000 utterances for a usable first voice
- 3000+ for better coverage/prosody
- Include numbers, names, commands, bedtime phrases, emotional cues

## 2. Recording Requirements

Use consistent studio conditions:

- Quiet room, low reverb, constant mic distance
- Single microphone + interface across all sessions
- 16-bit PCM WAV mono
- Fixed sample rate per corpus (recommended: `24000` or `48000`)
- No clipping, no noise suppression artifacts

Target structure:

```text
work/henry_voice/
  wav/
    000001.wav
    000002.wav
    ...
  text.csv          # id|transcript
  metadata.md       # session notes, mic, room, date
```

`text.csv` example:

```text
000001|Hello, I am Henry. I am right here with you.
000002|Let's take a slow breath together.
```

## 3. Data QA Before Training

Minimum checks:

- 100% transcript/audio ID match
- No empty clips
- No clipped waveforms
- No long leading/trailing silence
- Consistent loudness

Hold out a fixed eval set (for example, 100 lines) and never train on it.

## 4. Labels And Linguistic Features

You need HTS labels for training.

This repo includes label generation utility source (`src/utils/make-hts-labels.cpp`), which can be used when built as:

- `AeonVoice-make-hts-labels`

If your build does not produce this binary, generate labels with your external HTS training toolchain.

## 5. Train External HTS Voice Models

Train duration/acoustic models in your HTS-compatible pipeline, then export model artifacts expected by AeonVoice.

For each target sample rate directory (commonly `16000/` and/or `24000/`), package:

- `voice.data`
- `dur.pdf`
- `mgc.pdf`
- `lf0.pdf`
- `bap.pdf`
- `mgc.win1`, `mgc.win2`, `mgc.win3`
- `lf0.win1`, `lf0.win2`, `lf0.win3`
- `bap.win1`, `bap.win2`, `bap.win3`
- `tree-dur.inf`, `tree-mgc.inf`, `tree-lf0.inf`, `tree-bap.inf`
- `bpf.txt`

Use existing voices in `data/voices/` as reference package layout.

## 6. Add The Voice To This Repo

Create:

```text
data/voices/<voice_id>/
  voice.info
  voice.params
  24000/
    ...
```

Example `voice.info`:

```ini
name=HenryWarm
language=English
gender=male
format=4
revision=1
```

Example `voice.params`:

```ini
beta=0.4
gain=1.0
key=173
```

## 7. Validate In Runtime

```bash
export AEONVOICE_DATA_PATH="$(pwd)/data"
export LD_LIBRARY_PATH="$(pwd)/build/linux/core:$(pwd)/build/linux/audio:$(pwd)/build/linux/lib"

echo "Hello, I am Henry. I am right here with you." \
  | build/linux/test/AeonVoice-test -p HenryWarm -o /tmp/henrywarm.wav

aplay /tmp/henrywarm.wav
```

## 8. Iterate Toward Character Quality

If voice identity is right but delivery is off:

- Tune runtime defaults (`rate`, `pitch`, `volume`) in your consuming app.

If timbre/prosody is still wrong:

- Add more targeted recordings for the missing emotional style.
- Retrain the model.

## 9. Versioning And Reuse

For portability across codebases:

- Store reference samples in `docs/voice-samples/<character>/`
- Keep a README with profile/parameters/scripts used
- Version voice model revisions using `revision=` in `voice.info`
