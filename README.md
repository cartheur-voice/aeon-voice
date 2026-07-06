# aeon-voice

[![NuGet Pack](https://github.com/cartheur-voice/aeon-voice/actions/workflows/nuget-pack.yml/badge.svg)](https://github.com/cartheur-voice/aeon-voice/actions/workflows/nuget-pack.yml)

The voice of artificial animals.

AeonVoice is a speaker-based TTS engine for giving invented creatures a believable voice.
In Aeon, we treat toys like characters: they greet, react, mutter, narrate, and occasionally surprise you.

## A Character Voice

<img src="images/toptygin.jpg" alt="Toptygin" width="220" />

Toptygin is one of those voices in spirit: warm, odd, and unmistakably alive.
The toy is still circuits, plastic, and code, but voice changes how it is perceived:
pauses become thought, intonation becomes mood, and small phrases become personality.
A character like Toptygin feels less like a device and more like a companion because
the voice carries presence, timing, and emotional texture.

---

This repo is both:
- an engineering toolchain you can drop into practical production workflows
- a creative instrument for shaping tone, rhythm, and personality in synthetic voices

## Repository layout

- `src/`: native engine, modules, utilities
- `data/`: runtime language/voice data used by synthesis
- `config/`: runtime configuration and dictionaries
- `doc/`: build and customization docs
- `dotnet/`: `AeonVoice` and `AeonVoice.Native` NuGet projects

## Build and run (native)

Prerequisites (Linux):
- `gcc/g++`
- `make`
- `scons`
- `pkg-config`

Build:

```bash
scons -j"$(nproc)"
```

Set runtime paths:

```bash
export AEONVOICE_DATA_PATH="$(pwd)/data"
export LD_LIBRARY_PATH="$(pwd)/build/linux/core:$(pwd)/build/linux/audio:$(pwd)/build/linux/lib"
```

Quick synthesis test:

```bash
echo "Hello from AeonVoice" | build/linux/test/AeonVoice-test -p Leena -o /tmp/sample.wav
```

## Voice/language work

For custom voices and training pipeline details, see:
- [Compilation](doc/Compilation.md)
- [Configuration](doc/Configuration.md)
- [Creating A Custom Voice](doc/CustomVoice.md)
- [Neural Voice Plan](docs/neural-voice-plan.md)
- [Neural Voice Architecture Notes](docs/neural-voice-architecture.md)
- [Neural Pilot Corpus](docs/neural-pilot-corpus.md)

## .NET and NuGet

Install from a .NET project:

```bash
dotnet add package AeonVoice
```

For packaging details and local packing commands, see:
- [dotnet/README.md](dotnet/README.md)

For the release runbook (versioning, tags, and publishing), see:
- [docs/releasing.md](docs/releasing.md)

## License

This repository is licensed under GNU GPL v3 (see `LICENSE`).
