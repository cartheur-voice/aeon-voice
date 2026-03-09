# .NET and NuGet packaging scaffold

This directory contains a starter layout to publish AeonVoice for .NET consumers.

## Projects

- `AeonVoice.Native`: native runtime assets package (`runtimes/<rid>/native/*`)
- `AeonVoice`: managed wrapper package that P/Invokes the native library

## Suggested workflow

1. Build native libraries with your normal build.
2. Stage `.so` files into the native package:

```bash
./dotnet/scripts/stage-native.sh linux-x64 ./build/linux
```

3. Pack native package:

```bash
dotnet pack dotnet/AeonVoice.Native/AeonVoice.Native.csproj -c Release
```

4. Pack managed package:

```bash
dotnet pack dotnet/AeonVoice/AeonVoice.csproj -c Release
```

## Consumption

From another .NET project:

```bash
dotnet add package AeonVoice
```

Then use `AeonVoiceEngine` to synthesize text to PCM16 samples.

## GitHub Actions

CI workflow: `.github/workflows/nuget-pack.yml`

- Builds native libraries for `linux-x64` and `linux-arm64`
- Packs `AeonVoice.Native` and `AeonVoice`
- Uploads `.nupkg` artifacts on PR/push
- Publishes to NuGet.org on `v*` tags or manual dispatch with `publish=true`

Set repository secret `NUGET_API_KEY` before publishing.

Publishing in CI requires:

- `NUGET_API_KEY`: NuGet.org API key with push permissions
