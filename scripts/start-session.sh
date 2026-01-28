#!/usr/bin/env bash
set -euo pipefail

ROOT="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
CERES_HOME="${CERES_HOME:-$ROOT/.ceres}"

# Auto-bootstrap if available (non-blocking).
if [[ -x "$CERES_HOME/bin/autobootstrap" ]]; then
  set +e
  "$CERES_HOME/bin/autobootstrap" >/dev/null 2>&1
  set -e
elif [[ -x "$ROOT/scripts/autobootstrap.sh" ]]; then
  set +e
  "$ROOT/scripts/autobootstrap.sh" >/dev/null 2>&1
  set -e
fi

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
