# aeon-voice

The voice of artificial animals.

## Background

This project has been laboring under an 8-bit voice that was fit-for-purpose but now we want to move beyond.

This repo is all about this evolution.

## The theory

There were two constructs we wanted to employ for this feature:

1. The simplest yet powerful speech synthesis,
2. Voices based on actual speakers and not AI.

For the former, the selection was to leverage the [statistical parametric synthesis](https://en.wikipedia.org/wiki/Speech_synthesis#HMM-based_synthesis) model in the context of [HTS](https://hts.sp.nitech.ac.jp).

Voices are built from recordings of natural speech, as such they have small footprints since the statistical models are stored on the Aeon hardware. Although it could be argued the voices lack the naturalness of the synthesizers - as a matter of speech generation by combining segments of the recordings themselves - these are still intelligible and resemble the speakers who recorded the source material, which is the point to bring _humanness_ to our artificial animals as [emotional](https://emotional.toys) toys.

## Documentation about the code

* [Compilation](/doc/Compilation.md)
* [Configuration](/doc/Configuration.md)
* [Creating A Custom Voice](/doc/CustomVoice.md)

## How to create a voice

For this quick workflow, "create a voice" means selecting a base speaker profile and tuning
prosody (rate, pitch, volume) for the toy persona.

If you want to train a truly new voice identity from your own recordings, follow:
`/doc/CustomVoice.md`

Custom voice training utilities are built with:

```bash
scons dev=True -j4
```

Debian training environment helper:

```bash
src/scripts/general/setup_environment_debian --help
```

Validation helper:

```bash
src/scripts/general/check_training_env.sh src/scripts/general/training.cfg
```

For custom training, also set required fields in `src/scripts/general/training.cfg`
(`wavedir`, `text`, `test`, `speaker`, `outdir`) as documented in `/doc/CustomVoice.md`.

### 1. Build the project

```bash
scons -j4
```

### 2. Set runtime environment

```bash
export AEONVOICE_DATA_PATH="$(pwd)/data"
export LD_LIBRARY_PATH="$(pwd)/build/linux/core:$(pwd)/build/linux/audio:$(pwd)/build/linux/lib"
```

### 3. Synthesize a candidate sample

```bash
echo "Hello, I am Henry. I am right here with you." \
  | build/linux/test/AeonVoice-test \
      -p Slt \
      -r 90 \
      -t 94 \
      -v 108 \
      -o /tmp/henry-sample.wav
```

Parameters:
- `-p`: voice profile (examples: `Slt`, `Clb`, `Lyubov`, `Alan`, `Ksp`, `Evgeniy-Eng`)
- `-r`: rate (100 is default; lower is slower)
- `-t`: pitch (100 is default; lower is deeper)
- `-v`: volume (100 is default)

### 4. Listen and iterate

```bash
aplay /tmp/henry-sample.wav
```

Adjust `-r/-t/-v` until the tone matches the character.

### 5. Save reusable voice artifacts

Store approved samples in-repo so they can be reused by other codebases.

Current example set:
- `docs/voice-samples/henry/README.md`
- `docs/voice-samples/henry/*.wav`
