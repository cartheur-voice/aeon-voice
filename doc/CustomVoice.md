# Creating A Custom Voice

This guide is for creating a **new trained voice** (not only tuning `-r/-t/-v`).

## Scope

This repo includes:

1. HTS demo training scaffold in `src/scripts/hts/`
2. AeonVoice voice-building helpers in `src/scripts/general/voice-building-utils`
3. Runtime integration/validation in AeonVoice itself

Training still depends on external toolchains (HTK/SPTK/Festival/HTS binaries).

## 0. Prerequisites

Build AeonVoice in development mode so helper binaries are produced:

```bash
scons dev=True -j4
```

`dev=True` is required for:

- `local/bin/AeonVoice-make-hts-labels`
- `local/bin/AeonVoice-transcribe-sentences`

Optional Debian helper (recommended):

```bash
src/scripts/general/setup_environment_debian \
  --workdir /opt/aeonvoice-train \
  --htk-bindir /opt/aeonvoice-train/htk341/bin \
  --hts22-bindir /opt/aeonvoice-train/hts22/bin
```

Validate environment at any time:

```bash
src/scripts/general/check_training_env.sh src/scripts/general/training.cfg
```

Fill required training config fields before running the helper workflow:

```bash
jq '
  .wavedir="/absolute/path/to/recordings" |
  .text="/absolute/path/to/train.ssml" |
  .test="/absolute/path/to/test.ssml" |
  .speaker="henrywarm" |
  .outdir="/absolute/path/to/aeon-voice/data/voices"
' src/scripts/general/training.cfg > /tmp/training.cfg && \
mv /tmp/training.cfg src/scripts/general/training.cfg
```

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

## 4. Initialize Training Workspace

Create an empty workspace and initialize the HTS scaffold:

```bash
mkdir -p work/henry-train
cd work/henry-train
python3 ../../src/scripts/general/voice-building-utils init
```

This copies the HTS training skeleton and default config into the workspace.

Required `training.cfg` fields used by `voice-building-utils`:

- `wavedir`
- `text`
- `test`
- `speaker`
- `language`
- `outdir`

## 5. Labels And Linguistic Features

You need HTS labels for training.

This repo includes label generation utility source (`src/utils/make-hts-labels.cpp`), which can be used when built as:

- `AeonVoice-make-hts-labels`

Generate labels and supporting files:

```bash
python3 ../../src/scripts/general/voice-building-utils label
```

## 6. Train HTS Voice Models

Run HTS training from the initialized workspace:

```bash
./configure
make
```

Or use helper subcommands from `voice-building-utils` for staged workflows
(`segment`, `extract-f0`, `make-questions`, `realign`, `export-voice`).

After training/export, package artifacts expected by AeonVoice.

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

## 7. Add The Voice To This Repo

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

## 8. Validate In Runtime

```bash
export AEONVOICE_DATA_PATH="$(pwd)/data"
export LD_LIBRARY_PATH="$(pwd)/build/linux/core:$(pwd)/build/linux/audio:$(pwd)/build/linux/lib"

echo "Hello, I am Henry. I am right here with you." \
  | build/linux/test/AeonVoice-test -p HenryWarm -o /tmp/henrywarm.wav

aplay /tmp/henrywarm.wav
```

## 9. Iterate Toward Character Quality

If voice identity is right but delivery is off:

- Tune runtime defaults (`rate`, `pitch`, `volume`) in your consuming app.

If timbre/prosody is still wrong:

- Add more targeted recordings for the missing emotional style.
- Retrain the model.

## 10. Versioning And Reuse

For portability across codebases:

- Store reference samples in `docs/voice-samples/<character>/`
- Keep a README with profile/parameters/scripts used
- Version voice model revisions using `revision=` in `voice.info`
