#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

SRC_DIR="/data/data/com.termux/files/home/dev/cori/alchemy_lab/g900/artifacts"
DST_DIR="/data/data/com.termux/files/home/storage/downloads"

find "$SRC_DIR" -maxdepth 1 -type f -name '*.json' -exec cp -f {} "$DST_DIR"/ \;

echo "Copied JSON files to: $DST_DIR"
