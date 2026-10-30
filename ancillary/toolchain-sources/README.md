# AeonVoice Ancillary Toolchain Sources

This directory records two ways to assemble dependencies for AeonVoice custom
voice training:

- the generic, downloadable open-source stack in `scripts/`; and
- the **locally verified legacy HTS route** below, built from the archived
  `HTS-essentials` materials.

The latter is deliberately detailed. HTS 2.3 is old software and the build is
a collection of small compatibility decisions, not a dependable one-command
install on a current Linux system. Keeping those decisions here prevents a
future rebuild from repeating the same dead ends.

Build products belong in `out/toolchain/` and are ignored by Git. Do not add
the source archives, the HTK checkout, trained voices, or locally-built
binaries to this repository.

## Generic open-source route

The scripts below fetch and build the components which may be redistributed
under their respective open-source licences:

```bash
cd ancillary/toolchain-sources
./scripts/fetch_open_sources.sh
./scripts/build_open_sources.sh
```

The default prefix is `ancillary/toolchain-sources/out/toolchain`. Override it
if needed:

```bash
PREFIX=/opt/aeonvoice-toolchain ./scripts/build_open_sources.sh
```

This route is not a substitute for the HTS 2.3 compatibility recipe below.

## Verified legacy HTS 2.3 route

### What is needed

Keep these user-acquired archives together outside this repository, for
example in `../HTS-essentials/`. The listed SHA-256 values identify the local
source artifacts used for the build and make it possible to detect an
accidental replacement.

| File | SHA-256 | Used for |
| --- | --- | --- |
| `HTK-3.4.1.tar.gz` | `42297b036ce3a47adeab26aaa42f51ac4b370ead7f53bab75fd27a52d38ae5ac` | HTK base source |
| `HDecode-3.4.1.tar.gz` | `9517b25a91200e3e84ebed0d615f73715196dbfaf32ef854c2e964442175bee5` | Source required while applying the HTS patch |
| `HTS-2.3_for_HTK-3.4.1.tar.bz2` | `9fe2480f834a1b4c124abaef6fee423530a8a6de79015413f3ca1d1fdc7644de` | HTS extensions for HTK |
| unpacked `SPTK-3.11/` source tree | local archive/source checksum: `ae26929a3c196ca8a1d1a638718fc4400adf8ce963b8328be72f8802f1589100` | `mcep`, `pitch`, and related signal tools |
| `hts_engine_API-1.10.tar.gz` | `e2132be5860d8fb4a460be766454cfd7c3e21cf67b509c48e1804feab14968f7` | HTS engine utility |
| `speech_tools-2.5.0-release.tar.gz` | `e4fd97ed78f14464358d09f36dfe91bc1721b7c0fa6503e04364fb5847805dcc` | Festival dependency |
| `festival-2.5.0-release.tar.gz` | `4c9007426b125290599d931df410e2def51e68a8aeebd89b4a61c7c96c09a4b4` | Festival label-generation dependency |

HTK and HDecode remain licence-gated. Obtain them legitimately, retain the
bundled licence, and accept it before use. A source mirror is only suitable
when it preserves that licence; this project neither fetches nor redistributes
those components. See [HTK_MANUAL.md](docs/HTK_MANUAL.md) for the narrower
HTK-only builder.

On Debian/Ubuntu, install the currently missing legacy prerequisites first:

```bash
sudo apt-get update
sudo apt-get install csh praat libncurses-dev
```

The normal compiler, make, Perl, Tcl/Tk, SoX, Python 3, `jq`, `patch`, and
development headers must already be available. This route is CPU-only; it does
not require CUDA or a GPU.

### Build order and destination

Use a clean temporary directory for each source build. The verified local
prefix is:

```text
ancillary/toolchain-sources/out/toolchain/
  hts23/bin/                 patched HTK + HTS training tools
  SPTK-3.11/bin/             mcep, pitch, and SPTK tools
  hts_engine_API-1.10/bin/   hts_engine
  speech_tools-2.5.0/        Festival's sibling dependency
  festival-2.5.0/            Festival plus examples/
```

Build in this order: patched HTK/HTS, SPTK, HTS Engine, Speech Tools, then
Festival. The commands below are intentionally explicit, because a generic
autotools invocation is not reliable for this vintage of code.

The examples assume they are run from `ancillary/toolchain-sources` and set
these two paths once. Keeping the build tree in `/tmp` means source archives
and manually acquired checkouts remain unmodified.

```bash
toolchain_dir="$PWD"
sources_dir="$(realpath ../HTS-essentials)"
build_dir="$(mktemp -d)"
trap 'rm -rf "$build_dir"' EXIT
```

#### 1. Patched HTK 3.4.1 / HTS 2.3

Unpack HTK, unpack HDecode *into the HTK tree*, then apply the HTS patch. The
HDecode files are needed for patch context even though `hdecode` itself is not
needed by AeonVoice training.

```bash
tar -xzf "$sources_dir/HTK-3.4.1.tar.gz" -C "$build_dir"
cd "$build_dir/htk"
tar -xzf "$sources_dir/HDecode-3.4.1.tar.gz"
mkdir "$build_dir/hts-patch"
tar -xjf "$sources_dir/HTS-2.3_for_HTK-3.4.1.tar.bz2" -C "$build_dir/hts-patch"
patch -p1 < "$build_dir/hts-patch/HTS-2.3_for_HTK-3.4.1.patch"
./configure --prefix="$toolchain_dir/out/toolchain/hts23" --disable-hlmtools \
  CFLAGS='-DARCH=\"x86_64\"'
make -j"$(nproc)"
make install
```

The HTS-patched configure script leaves `ARCH` undefined on current Linux;
without `-DARCH=\"x86_64\"`, `HTKLib/esignal.c` fails to compile. Do **not**
run `make hdecode` as part of this build: its legacy 32-bit pointer casts fail
under modern 64-bit GCC, and AeonVoice does not use it. Verify the installed
training tools instead:

```bash
"$toolchain_dir/out/toolchain/hts23/bin/HHEd" -V
test -x "$toolchain_dir/out/toolchain/hts23/bin/HCompV"
test -x "$toolchain_dir/out/toolchain/hts23/bin/HVite"
```

The separate `scripts/install_htk_from_source.sh` builds an unpatched
HTK-only checkout. It is useful to validate a manual HTK source acquisition,
but does not replace this patched HTS build.

#### 2. SPTK 3.11

SPTK needs `csh` even though most of its build looks like ordinary C. On
modern GCC, the optional PostScript graph tool (`psgr`) also fails because its
header defines a global object. Change that declaration before building:

```c
/* bin/psgr/psgr.h */
struct bbmargin { /* existing members */ };
extern struct bbmargin bbm;

/* bin/psgr/psgr.c, after includes */
struct bbmargin bbm;
```

Then configure, build, and install SPTK in a clean copied or unpacked source
tree:

```bash
cp -a "$sources_dir/SPTK-3.11" "$build_dir/"
cd "$build_dir/SPTK-3.11"
./configure --prefix="$toolchain_dir/out/toolchain/SPTK-3.11"
make -j"$(nproc)"
make install
test -x "$toolchain_dir/out/toolchain/SPTK-3.11/bin/mcep"
test -x "$toolchain_dir/out/toolchain/SPTK-3.11/bin/pitch"
```

The edit is a GCC 10+ compatibility fix for an optional SPTK program;
retaining it in build notes is important, since otherwise a nearly-complete
build fails late and misleadingly.

#### 3. HTS Engine API 1.10

This component builds normally:

```bash
tar -xzf "$sources_dir/hts_engine_API-1.10.tar.gz" -C "$build_dir"
cd "$build_dir/hts_engine_API-1.10"
./configure --prefix="$toolchain_dir/out/toolchain/hts_engine_API-1.10"
make -j"$(nproc)"
make install
"$toolchain_dir/out/toolchain/hts_engine_API-1.10/bin/hts_engine" -h
```

#### 4. Speech Tools 2.5 and Festival 2.5

Festival expects Speech Tools at `../speech_tools`. Build Speech Tools first,
then place or symlink its completed tree as a sibling of the Festival source
tree. The old Speech Tools source defines `editline_history_file` twice on new
linkers. In `siod/editline.c`, make its declaration external:

```c
extern char *editline_history_file;
```

Build Speech Tools, serially if recovery is needed:

```bash
./configure
make -j"$(nproc)"
```

For Festival, pass the compatibility flag through the environment — **not** as
an argument after `./configure`, which that old configure script mistakes for
a host specification:

```bash
env CFLAGS='-Wno-error=implicit-int' ./configure
make
```

Run Festival's `make` serially. Its static archive build is not parallel-safe
on this toolchain; `make -j` can leave an incomplete `src/lib/libFestival.a`.
If that happened, recover before retrying the final `make`:

```bash
find . -name .buildlib_Festival -type f -delete
rm -f src/lib/libFestival.a
make -C src JUST_LIB=YES
make
```

The modern linker may also require the Festival static libraries to be grouped.
In `src/main/Makefile`, immediately after the two existing `include` lines,
add:

```make
LIBS := -Wl,--start-group $(LIBS) -Wl,--end-group
```

`bin/festival` is a successful build even if starting it warns that no default
voice is installed. The training pipeline needs Festival's Scheme programs and
`examples/`, not a stock speaking voice.

### Create the training executable directory

AeonVoice expects `HCompV`, `mcep`, and `pitch` in the same `bindir`; HTK/HTS
and SPTK naturally install them in different directories. Make an ignored
symlink staging directory after both builds:

```bash
mkdir -p "$toolchain_dir/out/toolchain/bin"
ln -sfn ../hts23/bin/HCompV "$toolchain_dir/out/toolchain/bin/HCompV"
ln -sfn ../SPTK-3.11/bin/mcep "$toolchain_dir/out/toolchain/bin/mcep"
ln -sfn ../SPTK-3.11/bin/pitch "$toolchain_dir/out/toolchain/bin/pitch"
```

For an installation at a different prefix, use the equivalent absolute paths.

### Wire it into AeonVoice and verify

Use a project- or speaker-specific copy of `src/scripts/general/training.cfg`;
do not fill in the generic template. Its relevant values should be:

```json
{
  "bindir": "/absolute/path/ancillary/toolchain-sources/out/toolchain/bin",
  "htk_bindir": "/absolute/path/ancillary/toolchain-sources/out/toolchain/hts23/bin",
  "hts22_bindir": "/absolute/path/ancillary/toolchain-sources/out/toolchain/hts23/bin",
  "festdir": "/absolute/path/ancillary/toolchain-sources/out/toolchain/festival-2.5.0",
  "praat_path": "/usr/bin/praat"
}
```

Validate the result before launching a training run:

```bash
src/scripts/general/check_training_env.sh /path/to/speaker-training.cfg
```

That check also confirms the locally built AeonVoice label and transcription
helpers plus Python's `numpy`, `scipy`, and `pyworld` dependencies. On current
Debian, the system Python is externally managed, so install these in the
ignored toolchain virtual environment rather than with a system-wide `pip`
command:

```bash
python3 -m venv out/venv
out/venv/bin/python -m pip install numpy scipy pyworld 'setuptools<81'
PATH="$PWD/out/venv/bin:$PATH" \
  ../../src/scripts/general/check_training_env.sh /path/to/speaker-training.cfg
```

PyWorld 0.3.5 currently imports `pkg_resources`; pinning `setuptools<81`
provides that compatibility module on Python 3.13. A passing check means the
toolchain paths are coherent; it does not assess corpus quality, alignment
quality, or how natural the eventual HTS voice will sound.
