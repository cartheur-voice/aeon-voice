# HTK Manual Step

HTK is license-gated and should be acquired manually.

## 1. Download HTK

- Register and download from: https://htk.eng.cam.ac.uk/download.shtml

Typical binaries needed by AeonVoice training:

- `HLEd`
- `HVite`

## 2. Build/Install HTK

Install into a dedicated prefix, for example:

- `/opt/aeonvoice-toolchain/htk341/bin`

## 3. Wire Into AeonVoice Training Config

Set in `src/scripts/general/training.cfg`:

- `htk_bindir`: path containing `HLEd` and `HVite`

Also configure:

- `bindir`: path containing `HCompV`, `mcep`, `pitch`
- `hts22_bindir`: path containing `HHEd`
- `festdir`: Festival directory with `examples/`
- `praat_path`: full path to `praat` executable
