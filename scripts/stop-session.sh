#!/usr/bin/env bash
set -euo pipefail

PID_FILE="logs/handover-watch.pid"

if [[ ! -f "$PID_FILE" ]]; then
  echo "no handover watch pid file found"
  exit 0
fi

PID="$(cat "$PID_FILE")"
if [[ -n "$PID" ]] && kill -0 "$PID" 2>/dev/null; then
  kill "$PID"
  echo "stopped handover watch (pid $PID)"
else
  echo "handover watch not running"
fi

rm -f "$PID_FILE"
