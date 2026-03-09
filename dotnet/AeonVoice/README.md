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

using var engine = new AeonVoiceEngine(
    dataPath: "/path/to/aeonvoice/data",
    configPath: "/path/to/aeonvoice/config");

SynthesisResult result = engine.SynthesizeToPcm16(
    text: "Hello from AeonVoice",
    voiceProfile: "Leena");
```

`result.SampleRate` is the output sample rate.  
`result.Samples` is signed 16-bit mono PCM.

## Voice profiles (English female renamed)

- `Leena` (was `Slt`)
- `Helen` (was `Clb`)
- `Daria` (was `Lyubov`)

## Runtime data requirements

This package does **not** bundle language/voice resource packs by default.

You must provide AeonVoice runtime resources via:

1. Constructor paths (`dataPath`, `configPath`), or
2. Environment variables:
   - `AEONVOICE_DATA_PATH`
   - `AEONVOICE_CONFIG_PATH`

If resources are missing, engine initialization will fail.

## Troubleshooting

### `DllNotFoundException` / native load failures
- Confirm your RID is supported (`linux-x64` / `linux-arm64`).
- Confirm native assets are present from `AeonVoice.Native`.
- On Linux, verify dependency resolution for `.so` files.

### Engine creation fails
- Verify valid resource folders.
- Ensure selected voice profile exists in your installed data.

## License

See repository license files and voice/resource-specific licenses.
