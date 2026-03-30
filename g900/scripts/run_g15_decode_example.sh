#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

cd "$(dirname "$0")/.."
mkdir -p artifacts

python3 scripts/g15_cocycle_decode.py \
  --syndrome 0000000000000000 \
  --json-out artifacts/g15_decode_example.json
