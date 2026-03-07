#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
root_dir="$(realpath "$script_dir/..")"

# shellcheck disable=SC1091
source "$root_dir/manifests/sources.env"

mkdir -p "$root_dir/sources"

fetch() {
  local url="$1"
  local out="$2"
  if [[ -f "$out" ]]; then
    echo "skip: $out already exists"
    return
  fi
  echo "fetch: $url"
  curl -L --fail --retry 3 --retry-delay 2 -o "$out" "$url"
}

fetch "$SPTK_URL" "$root_dir/sources/SPTK-${SPTK_VERSION}.tar.gz"
fetch "$HTS_ENGINE_API_URL" "$root_dir/sources/hts_engine_API-${HTS_ENGINE_API_VERSION}.tar.gz"
fetch "$FESTIVAL_URL" "$root_dir/sources/festival-master.tar.gz"
fetch "$SPEECH_TOOLS_URL" "$root_dir/sources/speech_tools-master.tar.gz"

echo "done: open-source source archives fetched into $root_dir/sources"
echo "next: run ./scripts/verify_sources.sh (optional), then ./scripts/build_open_sources.sh"
