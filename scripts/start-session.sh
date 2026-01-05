#!/usr/bin/env bash
set -euo pipefail

LOG_DIR="logs"
PID_FILE="$LOG_DIR/handover-watch.pid"
LOG_FILE="$LOG_DIR/handover-watch.log"

mkdir -p "$LOG_DIR"

if [[ -f "$PID_FILE" ]]; then
  PID="$(cat "$PID_FILE")"
  if [[ -n "$PID" ]] && kill -0 "$PID" 2>/dev/null; then
    echo "handover watch already running (pid $PID)"
    exit 0
  fi
fi

nohup ./scripts/export-handover.py --watch > "$LOG_FILE" 2>&1 &
PID=$!

echo "$PID" > "$PID_FILE"

echo "started handover watch (pid $PID)"
