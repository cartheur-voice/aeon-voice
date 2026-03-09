#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 2 ]]; then
  echo "Usage: $0 <rid> <build-root-dir>"
  echo "Example: $0 linux-x64 ./build/linux"
  exit 1
fi

RID="$1"
BUILD_ROOT_DIR="$2"

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
NATIVE_DIR="$SCRIPT_DIR/../AeonVoice.Native/runtimes/$RID/native"

if [[ ! -d "$BUILD_ROOT_DIR" ]]; then
  echo "Build root does not exist: $BUILD_ROOT_DIR"
  exit 1
fi

mkdir -p "$NATIVE_DIR"
rm -f "$NATIVE_DIR"/*

PATTERNS=(
  "libAeonVoice.so*"
  "libAeonVoice_core.so*"
  "libAeonVoice_audio.so*"
  "libhts_engine.so*"
)

staged=0
for pattern in "${PATTERNS[@]}"; do
  while IFS= read -r -d '' lib; do
    cp -af "$lib" "$NATIVE_DIR/"
    staged=1
  done < <(find "$BUILD_ROOT_DIR" -type f -name "$pattern" -print0)

  while IFS= read -r -d '' lib; do
    cp -af "$lib" "$NATIVE_DIR/"
    staged=1
  done < <(find "$BUILD_ROOT_DIR" -type l -name "$pattern" -print0)
done

if [[ "$staged" -eq 0 ]]; then
  echo "No native libraries were staged from $BUILD_ROOT_DIR"
  exit 1
fi

echo "Staged native libraries to: $NATIVE_DIR"
ls -la "$NATIVE_DIR"
