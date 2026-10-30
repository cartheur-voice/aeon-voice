#!/usr/bin/env bash
set -euo pipefail

# HTK is acquired manually because its licence requires acceptance.  This
# script only builds an already-cloned or already-unpacked source tree.
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
root_dir="$(realpath "$script_dir/..")"
source_dir="${1:?usage: $0 /path/to/htk-source-tree}"
prefix="${PREFIX:-$root_dir/out/toolchain/htk341}"
jobs="${JOBS:-$(nproc)}"

if [[ ! -x "$source_dir/configure" || ! -d "$source_dir/HTKTools" ]]; then
  echo "not an HTK source tree: $source_dir" >&2
  exit 2
fi

build_dir="$(mktemp -d "${TMPDIR:-/tmp}/aeon-htk-build.XXXXXX")"
trap 'rm -rf "$build_dir"' EXIT

# Build outside the manually acquired checkout, keeping it clean and reusable.
cp -a "$source_dir/." "$build_dir/"
mkdir -p "$prefix"
pushd "$build_dir" >/dev/null
./configure --prefix="$prefix" --disable-hlmtools
make -j"$jobs"
make install
popd >/dev/null

for tool in HCompV HERest HHEd HVite HInit HRest; do
  if [[ ! -x "$prefix/bin/$tool" ]]; then
    echo "HTK install is incomplete: missing $prefix/bin/$tool" >&2
    exit 1
  fi
done

echo "HTK 3.4.1 tools installed in: $prefix/bin"
