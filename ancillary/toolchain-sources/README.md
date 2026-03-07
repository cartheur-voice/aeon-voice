# AeonVoice Ancillary Toolchain Sources

This folder is a scaffold for a separate repository that acquires and builds
open-source dependencies used in AeonVoice custom voice training.

## Scope

- Fetch open-source toolchain sources with pinned versions.
- Build/install those sources into a local prefix.
- Keep HTK as a manual, license-gated step.

## Layout

- `manifests/sources.env`: version pins and source URLs
- `scripts/fetch_open_sources.sh`: download/open-source fetch
- `scripts/build_open_sources.sh`: build/install open-source components
- `scripts/verify_sources.sh`: validate source tarballs with checksums (optional)
- `docs/HTK_MANUAL.md`: manual HTK acquisition/install instructions

## Quick Start

```bash
cd ancillary/toolchain-sources
./scripts/fetch_open_sources.sh
./scripts/build_open_sources.sh
```

Default install prefix:

- `ancillary/toolchain-sources/out/toolchain`

You can override:

```bash
PREFIX=/opt/aeonvoice-toolchain ./scripts/build_open_sources.sh
```

## HTK Note

HTK is not auto-fetched by design. See:

- `docs/HTK_MANUAL.md`
