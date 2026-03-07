#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
root_dir="$(realpath "$script_dir/..")"

# shellcheck disable=SC1091
source "$root_dir/manifests/sources.env"

check_sha() {
  local file="$1"
  local sha="$2"
  if [[ -z "$sha" ]]; then
    echo "warn: no checksum configured for $(basename "$file")"
    return
  fi
  echo "$sha  $file" | sha256sum -c -
}

check_sha "$root_dir/sources/SPTK-${SPTK_VERSION}.tar.gz" "$SPTK_SHA256"
check_sha "$root_dir/sources/hts_engine_API-${HTS_ENGINE_API_VERSION}.tar.gz" "$HTS_ENGINE_API_SHA256"
check_sha "$root_dir/sources/festival-master.tar.gz" "$FESTIVAL_SHA256"
check_sha "$root_dir/sources/speech_tools-master.tar.gz" "$SPEECH_TOOLS_SHA256"

echo "done: checksum verification complete"
