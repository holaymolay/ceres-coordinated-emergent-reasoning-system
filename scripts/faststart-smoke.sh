#!/usr/bin/env bash
set -euo pipefail

ROOT="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
CERES_HOME="$ROOT/.ceres"
WORKSPACE="$CERES_HOME/workspace"

fail() { echo "FAIL: $*" >&2; exit 1; }

[[ -x "$CERES_HOME/bin/autobootstrap" ]] || fail "autobootstrap missing"
"$CERES_HOME/bin/autobootstrap" >/dev/null 2>&1 || true

for path in \
  "$CERES_HOME/core" \
  "$CERES_HOME/bin" \
  "$WORKSPACE/todo-inbox.md" \
  "$WORKSPACE/todo.md" \
  "$WORKSPACE/completed.md" \
  "$WORKSPACE/memory.md" \
  "$WORKSPACE/handover.md" \
  "$WORKSPACE/objective-contract.json" \
  "$WORKSPACE/gap-ledger.json" \
  "$WORKSPACE/specs/elicitation/elicitation.md"; do
  [[ -e "$path" ]] || fail "missing: $path"
done

PID_FILE="$ROOT/logs/handover-watch.pid"
if [[ -f "$PID_FILE" ]]; then
  PID="$(cat "$PID_FILE")"
  if [[ -n "$PID" ]] && kill -0 "$PID" 2>/dev/null; then
    echo "FAST_START smoke check passed."
    exit 0
  fi
fi

fail "handover watch not running"
