# AeonVoice.Native

This package carries native binaries used by the managed `AeonVoice` package.

## Included runtime identifiers

- `linux-x64`
- `linux-arm64`

## Notes

- Place shared libraries under `runtimes/<rid>/native/` before running `dotnet pack`.
- Typical primary binary name: `libAeonVoice.so`.
- Depending on how you build AeonVoice, dependent libraries may also be required.
