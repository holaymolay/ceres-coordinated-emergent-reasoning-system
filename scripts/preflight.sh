#!/usr/bin/env bash
set -euo pipefail

ROOT="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"

MODE="execute"
PROMPT_FILE="todo-inbox.md"
REPORT_FILE="$ROOT/logs/prompt-debug-report.yaml"
TODO_FILE="todo.md"
GAP_LEDGER="gap-ledger.json"
OBJECTIVE="objective-contract.json"
TASK_ID=""

usage() {
  cat <<'USAGE'
Usage: ./scripts/preflight.sh [options]

Options:
  --mode <plan|execute>       Gate mode (default: execute)
  --prompt <path>             Prompt file (default: todo-inbox.md)
  --prompt-report <path>      Output path for Prompt Debug Report (default: logs/prompt-debug-report.yaml)
  --todo <path>               Task Plan path (default: todo.md)
  --gap-ledger <path>         Gap Ledger path (default: gap-ledger.json)
  --objective <path>          Objective Contract path (default: objective-contract.json)
  --task-id <id>              Optional task identifier for logging
USAGE
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --mode)
      MODE="$2"; shift 2;;
    --prompt)
      PROMPT_FILE="$2"; shift 2;;
    --prompt-report)
      REPORT_FILE="$2"; shift 2;;
    --todo)
      TODO_FILE="$2"; shift 2;;
    --gap-ledger)
      GAP_LEDGER="$2"; shift 2;;
    --objective)
      OBJECTIVE="$2"; shift 2;;
    --task-id)
      TASK_ID="$2"; shift 2;;
    -h|--help)
      usage; exit 0;;
    *)
      echo "Unknown option: $1" >&2; usage; exit 1;;
  esac
 done

if [[ "$MODE" != "plan" && "$MODE" != "execute" ]]; then
  echo "Invalid mode: $MODE (expected plan or execute)" >&2
  exit 1
fi

make_abs() {
  local path="$1"
  if [[ "$path" = /* ]]; then
    echo "$path"
  else
    echo "$ROOT/$path"
  fi
}

PROMPT_FILE="$(make_abs "$PROMPT_FILE")"
REPORT_FILE="$(make_abs "$REPORT_FILE")"
TODO_FILE="$(make_abs "$TODO_FILE")"
GAP_LEDGER="$(make_abs "$GAP_LEDGER")"
OBJECTIVE="$(make_abs "$OBJECTIVE")"

mkdir -p "$ROOT/logs"

if [[ ! -f "$PROMPT_FILE" ]]; then
  echo "Prompt file not found: $PROMPT_FILE" >&2
  exit 1
fi

"$ROOT/prompt-debugger/cli.py" --prompt-file "$PROMPT_FILE" > "$REPORT_FILE"

python - <<'PY' "$REPORT_FILE"
import json
import sys
from pathlib import Path

path = Path(sys.argv[1])
text = path.read_text(encoding="utf-8")

try:
    import yaml  # type: ignore
except Exception:
    yaml = None

data = None
if yaml is not None:
    try:
        data = yaml.safe_load(text)
    except Exception:
        data = None
if data is None:
    try:
        data = json.loads(text)
    except Exception as exc:
        raise SystemExit(f"Failed to parse Prompt Debug Report: {exc}")

status = (data or {}).get("status")
if status != "approved":
    raise SystemExit(f"Prompt Debug Report status is '{status}'. Resolve issues before proceeding.")
PY

if [[ ! -f "$OBJECTIVE" ]]; then
  echo "Objective Contract missing: $OBJECTIVE" >&2
  exit 1
fi

python - <<'PY' "$OBJECTIVE" "$MODE"
import json
import sys
from pathlib import Path

path = Path(sys.argv[1])
mode = sys.argv[2]
text = path.read_text(encoding="utf-8")

try:
    import yaml  # type: ignore
except Exception:
    yaml = None

data = None
if yaml is not None:
    try:
        data = yaml.safe_load(text)
    except Exception:
        data = None
if data is None:
    try:
        data = json.loads(text)
    except Exception as exc:
        raise SystemExit(f"Failed to parse Objective Contract: {exc}")

status = (data or {}).get("status")
if mode == "execute" and status != "committed":
    raise SystemExit(f"Objective Contract status must be 'committed' for execute mode (found '{status}').")
if mode == "plan" and status not in {"draft", "committed"}:
    raise SystemExit(f"Objective Contract status must be draft or committed for plan mode (found '{status}').")
PY

if [[ ! -f "$GAP_LEDGER" ]]; then
  echo "Gap Ledger missing: $GAP_LEDGER" >&2
  exit 1
fi

python - <<'PY' "$GAP_LEDGER" "$MODE"
import json
import sys
from pathlib import Path

path = Path(sys.argv[1])
mode = sys.argv[2]
text = path.read_text(encoding="utf-8")

try:
    import yaml  # type: ignore
except Exception:
    yaml = None

data = None
if yaml is not None:
    try:
        data = yaml.safe_load(text)
    except Exception:
        data = None
if data is None:
    try:
        data = json.loads(text)
    except Exception as exc:
        raise SystemExit(f"Failed to parse Gap Ledger: {exc}")

gaps = (data or {}).get("gaps")
if not isinstance(gaps, list):
    raise SystemExit("Gap Ledger must contain a 'gaps' list")

if mode == "execute":
    blocking = [g for g in gaps if isinstance(g, dict) and g.get("blocking") is True and g.get("status") != "resolved"]
    if blocking:
        ids = [g.get("gap_id", "<unknown>") for g in blocking]
        raise SystemExit(f"Blocking gaps unresolved: {', '.join(ids)}")
PY

if [[ ! -x "$ROOT/scripts/run-component.sh" ]]; then
  echo "Missing hub helper: $ROOT/scripts/run-component.sh" >&2
  exit 1
fi

LOG_HELPER="$ROOT/scripts/log_event.py"
CMD=("scripts/enforce-lifecycle.py"
  "--todo" "$TODO_FILE"
  "--gap-ledger" "$GAP_LEDGER"
  "--prompt-report" "$REPORT_FILE"
  "--require-ceres-todo"
  "--require-gap-ledger"
  "--validate-gap-ledger"
  "--require-todo-structure"
  "--log-helper" "$LOG_HELPER"
)

if [[ -n "$TASK_ID" ]]; then
  CMD+=("--task-id" "$TASK_ID")
fi

"$ROOT/scripts/run-component.sh" governance-orchestrator "${CMD[*]}"

echo "Preflight checks passed ($MODE mode)."
