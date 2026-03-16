# .NET and NuGet packaging

This directory contains the .NET packages used to distribute AeonVoice to .NET consumers.

## Projects

- `AeonVoice.Native`: native runtime package (`runtimes/<rid>/native/*`) plus bundled runtime resources.
- `AeonVoice`: managed wrapper package that P/Invokes AeonVoice native libraries.

## Local packaging workflow

1. Build native libraries:

```bash
scons -j"$(nproc)"
```

2. Stage native libraries into NuGet runtime folders:

```bash
./dotnet/scripts/stage-native.sh linux-x64 ./build/linux
./dotnet/scripts/stage-native.sh linux-arm64 ./build/linux
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

In another .NET project:

```bash
dotnet add package AeonVoice
```

`AeonVoice` depends on `AeonVoice.Native` automatically.

## CI and publishing

Workflow: `.github/workflows/nuget-pack.yml`

- Builds native assets for `linux-x64` and `linux-arm64`
- Packs `AeonVoice.Native` and `AeonVoice`
- Uploads `.nupkg` artifacts on PR/push
- Publishes on tag pushes `v*` (or manual dispatch with `publish=true`)

Trusted Publishing is used (OIDC via `NuGet/login@v1`), not static API key publishing.

Required repository secret:
- `NUGET_USER` (NuGet.org profile name used by `NuGet/login@v1`)

## Versioning behavior

- Tag push `vX.Y.Z` => package version `X.Y.Z`
- Non-tag runs => CI version `0.1.0-ci.<run_number>`
- Tags are not auto-incremented; each release requires a new tag push.

For a concrete release runbook, see [`docs/releasing.md`](../docs/releasing.md).
