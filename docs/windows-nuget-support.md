# Windows NuGet Support

AeonVoice's managed wrapper can load `AeonVoice.dll` on Windows, but the
NuGet package currently contains native assets only for Linux. Windows support
should be introduced as a `win-x64` runtime asset before considering
`win-arm64`.

## Required changes

1. Add a Windows native build job to `.github/workflows/nuget-pack.yml` using
   a GitHub `windows-2022` runner and the existing SCons Windows build path.
   The Windows SCons build includes `src/lib/lib.def` so the C API is exported
   from `AeonVoice.dll`.
2. Add Windows staging support. The current `dotnet/scripts/stage-native.sh`
   stages only Linux `.so` files; Windows staging must place all runtime DLLs
   in `dotnet/AeonVoice.Native/runtimes/win-x64/native/`.
3. Download the Windows native artifact in the pack job so
   `AeonVoice.Native` includes it through its existing `runtimes/**/*` item.
4. Add a Windows packaged-consumer smoke test that restores `AeonVoice` from
   the packed artifacts and synthesizes an English sample with the bundled
   Leena resources.
5. Verify exports and compilation with MSVC. Normalize platform checks where
   needed: the native code currently mixes `WIN32`, `_WIN32`, and `MSC_VER`.
6. Define and test the Microsoft C++ runtime policy on a clean Windows VM:
   statically link it or document/package the required Visual C++
   Redistributable.

## Release requirements

- Document `win-x64` in both NuGet package READMEs.
- Publish only after native build and packaged-consumer smoke tests succeed on
  Windows as well as the existing Linux RIDs.
- Treat the addition as a new NuGet release; published package versions cannot
  be replaced.
