# Next Session Prompt

We are continuing work on the AeonVoice .NET/NuGet packages.

The current package IDs and branding remain unchanged:

- `AeonVoice`
- `AeonVoice.Native`

The currently published version of both packages is `0.1.7`; the next release
version is `0.2.0`.

Do not plan, propose, or implement any Supertoys rebranding, migration, shim,
or package-graph work.

## Smoke-test goal

Make the release pipeline prove that a consumer can install only `AeonVoice`
from locally packed artifacts and synthesize speech without custom MSBuild copy
targets, library preloading, or manually supplied resource paths.

## Acceptance criteria

1. Pack `AeonVoice.Native` and `AeonVoice` with a matching test version.
2. Restore a clean, separate consumer project using only the local package feed
   plus NuGet.org for framework/runtime packs.
3. Test both `linux-x64` and `linux-arm64` in their corresponding CI jobs or
   runners.
4. For each RID, verify normal NuGet runtime selection places the native
   libraries in the application output under the conventional runtime assets
   flow—no application-specific copy target and no hard-coded project RID.
5. Verify the `AeonVoice.Native` `buildTransitive` target copies the bundled
   English/Leena/config assets into `AppContext.BaseDirectory/aeonvoice/`.
6. Create `AeonVoiceEngine` with default paths, synthesize a short phrase with
   `Leena`, and assert a positive sample rate and non-empty PCM output.
7. Write the result using `SynthesisResult.WriteWave`, then validate that the
   output is a non-empty PCM WAV file (at least the 44-byte header plus data).
8. Confirm native dependency loading works through the packaged `$ORIGIN`
   RUNPATH, without `LD_LIBRARY_PATH`, explicit `NativeLibrary.Load`, or other
   preloading.
9. Preserve the smoke-test WAV only as a CI/workspace artifact; do not publish
   it in a NuGet package.

## Follow-up work

- Review the existing GitHub Actions smoke-test step for clean-cache behavior
  and ensure it cannot accidentally consume project references or previously
  installed package versions.
- Add an ARM64 package-consumer smoke run if the current workflow only runs
  the x64 sample.
- Keep the managed API limited to PCM output and WAV encoding convenience;
  playback stays application-owned. Documentation may use `aplay` as a Linux
  example.
- Report the exact package paths, dependency metadata, copied resource paths,
  and `readelf` RUNPATH evidence in the validation summary.
