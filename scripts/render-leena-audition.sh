#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BUILD_DIR="${ROOT_DIR}/build/linux"
TEST_BIN="${BUILD_DIR}/test/AeonVoice-test"
OUT_DIR="${ROOT_DIR}/docs/voice-samples/leena"
CFG_ROOT="${OUT_DIR}/audition-configs"
MIDPOINT_TEXT_FILE="${OUT_DIR}/leena-midpoint.txt"
CONFIG_DIR="${ROOT_DIR}/config"

if [[ ! -x "${TEST_BIN}" ]]; then
  echo "Missing test binary: ${TEST_BIN}" >&2
  echo "Build first with: PYTHONPATH=/tmp/aeonvoice-pydeps python3 -m SCons -j2" >&2
  exit 1
fi

mkdir -p "${OUT_DIR}"

cat > "${MIDPOINT_TEXT_FILE}" <<'EOF'
Hello. I am Leena. I am here with you and can help with anything you may need.
I can tell a short story, ask a question, and pause before an important word.
Numbers like 7 and 42, and punctuation, should still sound calm and natural.
EOF

export LD_LIBRARY_PATH="${BUILD_DIR}/core:${BUILD_DIR}/audio:${BUILD_DIR}/lib"
export AEONVOICE_DATA_PATH="${ROOT_DIR}/data"

AEONVOICE_CONFIG_PATH="${CONFIG_DIR}" \
  "${TEST_BIN}" -i "${MIDPOINT_TEXT_FILE}" -p Leena -o "${OUT_DIR}/leena-midpoint.wav"

cat > "${OUT_DIR}/i-uppercase.txt" <<'EOF'
I am here. I am listening.
EOF

cat > "${OUT_DIR}/i-lowercase.txt" <<'EOF'
i am here. i am listening.
EOF

AEONVOICE_CONFIG_PATH="${CONFIG_DIR}" \
  "${TEST_BIN}" -i "${OUT_DIR}/i-uppercase.txt" -p Leena -o "${OUT_DIR}/leena-i-uppercase.wav"

AEONVOICE_CONFIG_PATH="${CONFIG_DIR}" \
  "${TEST_BIN}" -i "${OUT_DIR}/i-lowercase.txt" -p Leena -o "${OUT_DIR}/leena-i-lowercase.wav"

echo "Rendered samples:"
printf ' - %s\n' \
  "${OUT_DIR}/leena-midpoint.wav" \
  "${OUT_DIR}/leena-i-uppercase.wav" \
  "${OUT_DIR}/leena-i-lowercase.wav"
