#!/data/data/com.termux/files/usr/bin/bash
set -e

cd /data/data/com.termux/files/home/dev/cori/alchemy_lab/http
source ../.venv/bin/activate
exec uvicorn api_server:app --host 127.0.0.1 --port 8000
