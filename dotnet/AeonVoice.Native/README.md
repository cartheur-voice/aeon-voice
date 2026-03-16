# AeonVoice.Native

Native runtime assets for AeonVoice .NET consumption.

This package contains platform-specific shared libraries used by the managed `AeonVoice` package.

## Included runtimes

- `linux-x64`
- `linux-arm64`

## Package contents

Libraries are delivered under:

- `runtimes/linux-x64/native/`
- `runtimes/linux-arm64/native/`

Typical libraries include:

- `libAeonVoice.so*`
- `libAeonVoice_core.so*`
- `libAeonVoice_audio.so*`

## Usage

Install this package directly only if you are wiring interop manually.  
Most users should install `AeonVoice`, which references this package automatically.

## Important

`AeonVoice.Native` provides native binaries plus a minimal runtime data bundle:
- `data/languages/English`
- `data/voices/leena`
- `config/AeonVoice.conf`
- `config/dicts/english`

These files are packaged as `contentFiles` and copied to consumer output under `aeonvoice/` via `buildTransitive` targets.

## License

See repository license files and voice/resource-specific licenses.
