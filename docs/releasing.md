# Releasing AeonVoice NuGet Packages

This runbook documents the release flow for:
- `AeonVoice`
- `AeonVoice.Native`

CI workflow: `.github/workflows/nuget-pack.yml`

## Preconditions

- You are on `main` with a clean working tree.
- Changes to be released are committed and pushed.
- Repository secret `NUGET_USER` is configured for Trusted Publishing.

## Versioning rules

- Release version comes from the git tag:
  - `v0.1.7` -> package version `0.1.7`
- Non-tag CI runs produce CI versions:
  - `0.1.0-ci.<run_number>`
- Tags are not auto-generated.

## Release steps

1. Sync branch:

```bash
git checkout main
git pull --ff-only origin main
```

2. Create and push release tag:

```bash
git tag -a v0.1.8 -m "NuGet release v0.1.8"
git push origin v0.1.8
```

3. Monitor workflow:
- Open GitHub Actions and verify `NuGet Pack` run for the new tag.
- Confirm `publish` job succeeds.

4. Validate on NuGet:
- Confirm both `AeonVoice` and `AeonVoice.Native` show the new version.

## Optional local verification before tagging

```bash
scons -j"$(nproc)"
./dotnet/scripts/stage-native.sh linux-x64 ./build/linux
./dotnet/scripts/stage-native.sh linux-arm64 ./build/linux
dotnet pack dotnet/AeonVoice.Native/AeonVoice.Native.csproj -c Release
dotnet pack dotnet/AeonVoice/AeonVoice.csproj -c Release
```
