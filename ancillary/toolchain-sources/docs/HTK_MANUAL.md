# HTK Manual Step

HTK is license-gated and should be acquired manually. An HTK 3.4.1 source
mirror may be used only if its bundled HTK licence is retained and accepted.

## 1. Download HTK

- Register and download from: https://htk.eng.cam.ac.uk/download.shtml

Typical binaries needed by AeonVoice training:

- `HLEd`
- `HVite`

## 2. Build/Install HTK

Install into a dedicated prefix, for example:

- `/opt/aeonvoice-toolchain/htk341/bin`

The reproducible local builder keeps the source checkout unmodified:

```bash
./scripts/install_htk_from_source.sh /path/to/htk
```

It installs to `out/toolchain/htk341/bin` unless `PREFIX` is set.

## 3. Wire Into AeonVoice Training Config

Set in `src/scripts/general/training.cfg`:

- `htk_bindir`: path containing `HLEd` and `HVite`

Also configure:

- `bindir`: path containing `HCompV`, `mcep`, `pitch`
- `hts22_bindir`: path containing `HHEd`
- `festdir`: Festival directory with `examples/`
- `praat_path`: full path to `praat` executable
