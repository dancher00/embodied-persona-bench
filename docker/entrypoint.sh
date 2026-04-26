#!/usr/bin/env bash
set -euo pipefail

cleanup() {
  for pid in "${PIDS[@]:-}"; do
    if kill -0 "$pid" >/dev/null 2>&1; then
      kill "$pid" >/dev/null 2>&1 || true
    fi
  done
}

trap cleanup EXIT INT TERM

HOST_ADDR="${HOST_ADDR:-0.0.0.0}"
VIEWER_PORT="${VIEWER_PORT:-8765}"
API_PORT="${API_PORT:-8000}"
STREAMLIT_PORT="${STREAMLIT_PORT:-8501}"

python scripts/serve_urdf_viewer.py --host "$HOST_ADDR" --port "$VIEWER_PORT" &
PID_VIEWER=$!

python -m uvicorn tools.ratings_api:app --host "$HOST_ADDR" --port "$API_PORT" &
PID_API=$!

streamlit run tools/annotate_app.py --server.address "$HOST_ADDR" --server.port "$STREAMLIT_PORT" &
PID_STREAMLIT=$!

PIDS=("$PID_VIEWER" "$PID_API" "$PID_STREAMLIT")

wait -n "${PIDS[@]}"
