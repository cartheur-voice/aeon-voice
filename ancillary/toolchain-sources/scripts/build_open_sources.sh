#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
root_dir="$(realpath "$script_dir/..")"

# shellcheck disable=SC1091
source "$root_dir/manifests/sources.env"

PREFIX="${PREFIX:-$root_dir/out/toolchain}"
BUILD_DIR="$root_dir/build"
SRC_DIR="$root_dir/sources"
JOBS="${JOBS:-$(nproc)}"

mkdir -p "$BUILD_DIR" "$PREFIX"

extract() {
  local archive="$1"
  local out="$2"
  rm -rf "$out"
  mkdir -p "$out"
  tar -xf "$archive" -C "$out" --strip-components=1
}

build_speech_tools() {
  local dir="$BUILD_DIR/speech_tools"
  extract "$SRC_DIR/speech_tools-master.tar.gz" "$dir"
  pushd "$dir" >/dev/null
  ./configure --prefix="$PREFIX/speech_tools"
  make -j"$JOBS"
  make install
  popd >/dev/null
}

build_festival() {
  local dir="$BUILD_DIR/festival"
  extract "$SRC_DIR/festival-master.tar.gz" "$dir"
  pushd "$dir" >/dev/null
  ./configure --prefix="$PREFIX/festival"
  make -j"$JOBS"
  make install
  popd >/dev/null
}

build_sptk() {
  local dir="$BUILD_DIR/SPTK-${SPTK_VERSION}"
  extract "$SRC_DIR/SPTK-${SPTK_VERSION}.tar.gz" "$dir"
  pushd "$dir" >/dev/null
  ./configure --prefix="$PREFIX/SPTK-${SPTK_VERSION}"
  make -j"$JOBS"
  make install
  popd >/dev/null
}

build_hts_engine_api() {
  local dir="$BUILD_DIR/hts_engine_API-${HTS_ENGINE_API_VERSION}"
  extract "$SRC_DIR/hts_engine_API-${HTS_ENGINE_API_VERSION}.tar.gz" "$dir"
  pushd "$dir" >/dev/null
  ./configure --prefix="$PREFIX/hts_engine_api-${HTS_ENGINE_API_VERSION}"
  make -j"$JOBS"
  make install
  popd >/dev/null
}

for required in \
  "$SRC_DIR/speech_tools-master.tar.gz" \
  "$SRC_DIR/festival-master.tar.gz" \
  "$SRC_DIR/SPTK-${SPTK_VERSION}.tar.gz" \
  "$SRC_DIR/hts_engine_API-${HTS_ENGINE_API_VERSION}.tar.gz"; do
  if [[ ! -f "$required" ]]; then
    echo "missing source archive: $required" >&2
    echo "run: ./scripts/fetch_open_sources.sh" >&2
    exit 1
  fi
done

build_speech_tools
build_festival
build_sptk
build_hts_engine_api

cat <<EOF
done: open-source toolchain components installed
prefix: $PREFIX

next manual step:
  install HTK binaries separately (see docs/HTK_MANUAL.md)
EOF
