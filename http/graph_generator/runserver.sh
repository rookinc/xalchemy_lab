#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
cd "$HERE"

echo "Serving from: $HERE"
echo "Open: http://127.0.0.1:8000/lazy_universe_stepper.html"

python3 -m http.server 8000
