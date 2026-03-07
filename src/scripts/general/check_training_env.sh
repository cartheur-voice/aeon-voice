#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  check_training_env.sh [training_cfg_path]

Checks whether the custom voice training environment is usable.
Default config path: ./training.cfg
EOF
}

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  usage
  exit 0
fi

cfg_path="${1:-training.cfg}"
if [[ ! -f "$cfg_path" ]]; then
  echo "ERROR: training config not found: $cfg_path" >&2
  exit 1
fi

require_cmd() {
  if ! command -v "$1" >/dev/null 2>&1; then
    echo "ERROR: command not found: $1" >&2
    exit 1
  fi
}

require_file() {
  if [[ ! -x "$1" ]]; then
    echo "ERROR: missing executable: $1" >&2
    exit 1
  fi
}

require_cmd python3
require_cmd jq

bindir="$(jq -r '.bindir // empty' "$cfg_path")"
htk_bindir="$(jq -r '.htk_bindir // empty' "$cfg_path")"
hts22_bindir="$(jq -r '.hts22_bindir // empty' "$cfg_path")"
praat_path="$(jq -r '.praat_path // empty' "$cfg_path")"
festdir="$(jq -r '.festdir // empty' "$cfg_path")"

if [[ -z "$bindir" || -z "$htk_bindir" || -z "$hts22_bindir" || -z "$praat_path" || -z "$festdir" ]]; then
  echo "ERROR: training.cfg has empty required fields (bindir/htk_bindir/hts22_bindir/praat_path/festdir)" >&2
  exit 1
fi

require_file "$bindir/HCompV"
require_file "$bindir/mcep"
require_file "$bindir/pitch"
require_file "$htk_bindir/HLEd"
require_file "$htk_bindir/HVite"
require_file "$hts22_bindir/HHEd"

if [[ ! -x "$praat_path" ]]; then
  echo "ERROR: praat not executable: $praat_path" >&2
  exit 1
fi

if [[ ! -d "$festdir/examples" ]]; then
  echo "ERROR: festival examples dir missing: $festdir/examples" >&2
  exit 1
fi

echo "OK: training environment looks consistent."
