# aeon-voice

[![NuGet Pack](https://github.com/cartheur-voice/aeon-voice/actions/workflows/nuget-pack.yml/badge.svg)](https://github.com/cartheur-voice/aeon-voice/actions/workflows/nuget-pack.yml)

The voice of artificial animals.

AeonVoice is a speaker-based TTS engine for giving invented creatures a believable voice.
In Aeon, we treat toys like characters: they greet, react, mutter, narrate, and occasionally surprise you.

This repo is both:
- an engineering toolchain you can drop into practical production workflows
- a creative instrument for shaping tone, rhythm, and personality in synthetic voices

It includes:
- native engine code and runtime assets
- language and voice resources
- training/utility scripts
- .NET wrapper and NuGet packaging

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

## .NET and NuGet

Packages:
- `AeonVoice.Native`: native runtime package
- `AeonVoice`: managed wrapper package

Local packing:

```bash
./dotnet/scripts/stage-native.sh linux-x64 ./build/linux
./dotnet/scripts/stage-native.sh linux-arm64 ./build/linux

dotnet pack dotnet/AeonVoice.Native/AeonVoice.Native.csproj -c Release
dotnet pack dotnet/AeonVoice/AeonVoice.csproj -c Release
```

Consumer install:

```bash
dotnet add package AeonVoice
```

## Release process

NuGet packaging and publishing is handled by:
- `.github/workflows/nuget-pack.yml`

Behavior:
- push to branch/PR: build + pack artifacts
- push tag `v*`: build + pack + publish to NuGet.org
- manual dispatch with `publish=true`: publish packed artifacts

Versioning:
- release version comes from the tag (for example `v0.1.7` -> `0.1.7`)
- non-tag runs use CI versions (`0.1.0-ci.<run_number>`)
- tags are not auto-incremented; each release requires pushing a new tag

Trusted Publishing:
- workflow uses OIDC (`NuGet/login@v1`)
- requires repo secret `NUGET_USER`

## License

This repository is licensed under GNU GPL v3 (see `LICENSE`).
