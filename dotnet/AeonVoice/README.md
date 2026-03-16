# AeonVoice

Managed .NET wrapper for the AeonVoice speech synthesis engine.

`AeonVoice` provides a simple C# API over the native AeonVoice runtime and returns PCM16 audio samples for playback or WAV encoding.

## Package relationship

- `AeonVoice` (this package): managed API + interop bindings.
- `AeonVoice.Native`: native runtime libraries for supported RIDs.

`AeonVoice` depends on `AeonVoice.Native`.

## Supported runtimes

Current packaged runtimes:

- `linux-x64`
- `linux-arm64`

## Install

```bash
dotnet add package AeonVoice
```

## Quick start

```csharp
using AeonVoice;

using var engine = new AeonVoiceEngine();

SynthesisResult result = engine.SynthesizeToPcm16(
    text: "Hello from AeonVoice",
    voiceProfile: "Leena");
```

`result.SampleRate` is the output sample rate.  
`result.Samples` is signed 16-bit mono PCM.

## Voice profiles (English female)

- `Leena`

## Runtime data requirements

This package now includes a minimal runtime data set for `Leena` voice and English language resources.

By default, `AeonVoiceEngine` auto-detects packaged resources from the application output directory:

1. `./aeonvoice/data`
2. `./aeonvoice/config`

These files are copied automatically by NuGet build targets from `AeonVoice.Native`.

If you store resources elsewhere, you can override with constructor args:

```csharp
using var engine = new AeonVoiceEngine(
    dataPath: "/custom/path/data",
    configPath: "/custom/path/config");
```

Or environment variables:

- `AEONVOICE_DATA_PATH`
- `AEONVOICE_CONFIG_PATH`

If resources are missing or you use a different voice pack, engine initialization will fail.

## Troubleshooting

### `DllNotFoundException` / native load failures
- Confirm your RID is supported (`linux-x64` / `linux-arm64`).
- Confirm native assets are present from `AeonVoice.Native`.
- On Linux, verify dependency resolution for `.so` files.

### Engine creation fails
- Verify `aeonvoice/data` and `aeonvoice/config` exist under your app output.
- Ensure selected voice profile exists in installed resources (`Leena` is bundled).

## License

See repository license files and voice/resource-specific licenses.
