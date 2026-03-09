# AeonVoice

Managed .NET wrapper for the AeonVoice native library.

## Quick start

```csharp
using AeonVoice;

using var engine = new AeonVoiceEngine(dataPath: "/path/to/data", configPath: "/path/to/config");
SynthesisResult result = engine.SynthesizeToPcm16("Hello from AeonVoice", voiceProfile: "Slt");
```

`result.Samples` contains 16-bit PCM mono samples and `result.SampleRate` is the sample rate selected by the engine.

## Runtime data

AeonVoice requires language and voice data to be available at runtime. Configure one of:

- constructor `dataPath` / `configPath`
- `AEONVOICE_DATA_PATH`
- `AEONVOICE_CONFIG_PATH`
