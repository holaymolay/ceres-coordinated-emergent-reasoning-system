#!/usr/bin/env bash
set -euo pipefail

ROOT="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
if [[ "$ROOT" == *"/.ceres/"* || "$ROOT" == */.ceres ]]; then
  prefix="${ROOT%%/.ceres*}"
  if [[ -n "$prefix" ]]; then
    ROOT="$prefix"
  fi
fi
if [[ -n "${CERES_HOME:-}" && "$CERES_HOME" == */.ceres ]]; then
  ROOT="$(CDPATH= cd -- "${CERES_HOME%/.ceres}" && pwd)"
fi
CERES_HOME="${CERES_HOME:-$ROOT/.ceres}"

if [[ -f "$ROOT/scripts/auto-governance.py" ]]; then
  if command -v python3 >/dev/null 2>&1; then
    set +e
    python3 "$ROOT/scripts/auto-governance.py" >/dev/null 2>&1
    status=$?
    set -e
    if [[ "$status" -ne 0 ]]; then
      echo "WARN: auto-governance failed (non-blocking)." >&2
    fi
  else
    echo "WARN: auto-governance skipped (python3 missing)." >&2
  fi
fi

if command -v python3 >/dev/null 2>&1; then
  if [[ -f "$ROOT/scripts/preflight.py" ]]; then
    echo "INFO: preflight using python primary." >&2
    tmp_err="$(mktemp)"
    set +e
    python3 "$ROOT/scripts/preflight.py" "$@" 2> >(tee "$tmp_err" >&2)
    status=$?
    set -e
    if [[ "$status" -eq 0 ]]; then
      rm -f "$tmp_err"
      exit 0
    fi
    if grep -q -E "Traceback|SyntaxError|ModuleNotFoundError" "$tmp_err"; then
      echo "WARN: Python preflight failed (runtime error); falling back to shell." >&2
      rm -f "$tmp_err"
    else
      rm -f "$tmp_err"
      exit "$status"
    fi
  else
    echo "WARN: Python preflight missing; using shell fallback." >&2
  fi
else
  echo "WARN: python3 not found; using shell fallback." >&2
fi

MODE="execute"
PROMPT_FILE="todo-inbox.md"
REPORT_FILE="$ROOT/logs/prompt-debug-report.yaml"
TODO_FILE="todo.md"
GAP_LEDGER="gap-ledger.json"
OBJECTIVE="objective-contract.json"
ELICITATION="specs/elicitation"
TASK_ID=""
PHASE=""
AGENT=""
PATTERN=""
TASK_CLASS=""
EVENTS_FILE=""

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
  --elicitation <path>        Spec Elicitation path (default: specs/elicitation)
  --task-id <id>              Optional task identifier for logging
  --phase <name>              Active phase (default: planning for plan, execution for execute)
  --agent <name>              Active agent name (default: Planner for plan, Execution for execute)
  --pattern <name>            Active pattern name (default: planning for plan, tool-use for execute)
  --task-class <name>         Optional task class for reflection enforcement
  --events <path>             Observability events JSONL (default: logs/events.jsonl)
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
    --elicitation)
      ELICITATION="$2"; shift 2;;
    --task-id)
      TASK_ID="$2"; shift 2;;
    --phase)
      PHASE="$2"; shift 2;;
    --agent)
      AGENT="$2"; shift 2;;
    --pattern)
      PATTERN="$2"; shift 2;;
    --task-class)
      TASK_CLASS="$2"; shift 2;;
    --events)
      EVENTS_FILE="$2"; shift 2;;
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

if [[ -z "$PHASE" ]]; then
  if [[ "$MODE" == "plan" ]]; then
    PHASE="planning"
  else
    PHASE="execution"
  fi
fi

if [[ -z "$AGENT" ]]; then
  if [[ "$MODE" == "plan" ]]; then
    AGENT="Planner"
  else
    AGENT="Execution"
  fi
fi

if [[ -z "$PATTERN" ]]; then
  if [[ "$MODE" == "plan" ]]; then
    PATTERN="planning"
  else
    PATTERN="tool-use"
  fi
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
ELICITATION="$(make_abs "$ELICITATION")"
if [[ -n "$EVENTS_FILE" ]]; then
  EVENTS_FILE="$(make_abs "$EVENTS_FILE")"
fi

mkdir -p "$ROOT/logs"

policy_guard_advisory() {
  local guard="$ROOT/scripts/policy_guard.py"
  local policy="$ROOT/ceres.policy.yaml"
  if [[ ! -f "$guard" || ! -f "$policy" ]]; then
    return
  fi
  if ! command -v python3 >/dev/null 2>&1; then
    echo "WARN: policy guard advisory skipped (python3 missing)." >&2
    return
  fi
  set +e
  output="$(python3 "$guard" --current "$policy" 2>&1)"
  status=$?
  set -e
  if [[ -n "$output" ]]; then
    echo "INFO: policy guard advisory (non-blocking):" >&2
    echo "$output" >&2
  fi
  if [[ "$status" -ne 0 ]]; then
    echo "WARN: policy guard advisory detected errors (non-blocking)." >&2
  fi
}

policy_guard_advisory

workflow_guard_advisory() {
  local guard="$ROOT/scripts/workflow_guard.py"
  local workflow="$ROOT/ceres.workflow.yaml"
  if [[ -n "${CERES_WORKSPACE:-}" && -f "${CERES_WORKSPACE}/ceres.workflow.yaml" ]]; then
    workflow="${CERES_WORKSPACE}/ceres.workflow.yaml"
  fi
  if [[ ! -f "$guard" || ! -f "$workflow" ]]; then
    return
  fi
  if ! command -v python3 >/dev/null 2>&1; then
    echo "WARN: workflow guard advisory skipped (python3 missing)." >&2
    return
  fi
  set +e
  output="$(python3 "$guard" --current "$workflow" 2>&1)"
  status=$?
  set -e
  if [[ -n "$output" ]]; then
    echo "INFO: workflow guard advisory (non-blocking):" >&2
    echo "$output" >&2
  fi
  if [[ "$status" -ne 0 ]]; then
    echo "WARN: workflow guard advisory detected errors (non-blocking)." >&2
  fi
}

workflow_guard_advisory

if [[ ! -f "$PROMPT_FILE" ]]; then
  echo "Prompt file not found: $PROMPT_FILE" >&2
  exit 1
fi

PROMPT_DEBUGGER="$ROOT/prompt-debugger/cli.py"
if [[ ! -f "$PROMPT_DEBUGGER" && -f "$CERES_HOME/core/prompt-debugger/cli.py" ]]; then
  PROMPT_DEBUGGER="$CERES_HOME/core/prompt-debugger/cli.py"
fi
if [[ ! -f "$PROMPT_DEBUGGER" ]]; then
  echo "Prompt debugger not found: $PROMPT_DEBUGGER" >&2
  exit 1
fi

python3 "$PROMPT_DEBUGGER" --prompt-file "$PROMPT_FILE" > "$REPORT_FILE"

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

python - <<'PY' "$ELICITATION"
import sys
from pathlib import Path

path = Path(sys.argv[1])

def resolve(path):
    if path.is_dir():
        candidates = sorted(p for p in path.glob("*.md") if p.is_file())
        if not candidates:
            raise SystemExit(f"Spec Elicitation Record not found in {path}")
        if len(candidates) > 1:
            names = ", ".join(p.name for p in candidates)
            raise SystemExit(
                "Multiple Spec Elicitation Records found. Provide a single file or set --elicitation <path>. "
                f"Found: {names}"
            )
        return candidates[0]
    if not path.is_file():
        raise SystemExit(f"Spec Elicitation Record not found: {path}")
    return path


def parse_front_matter(text):
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise SystemExit("Spec Elicitation Record missing front matter (expected leading ---).")
    fm_lines = []
    for line in lines[1:]:
        if line.strip() == "---":
            break
        fm_lines.append(line)
    else:
        raise SystemExit("Spec Elicitation Record front matter not terminated (missing ---).")
    data = {}
    current_key = None
    for raw_line in fm_lines:
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" in line and not line.startswith("-"):
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip()
            current_key = None
            if value == "":
                data[key] = []
                current_key = key
            elif value in {"[]", "[ ]"}:
                data[key] = []
            elif value.lower() in {"true", "false"}:
                data[key] = value.lower() == "true"
            else:
                data[key] = value.strip("\"'")
        elif line.startswith("-") and current_key:
            item = line.lstrip("-").strip()
            if item:
                data.setdefault(current_key, []).append(item)
    return data


file_path = resolve(path)
data = parse_front_matter(file_path.read_text(encoding="utf-8"))
spec_id = data.get("spec_id")
if not isinstance(spec_id, str) or not spec_id.strip():
    raise SystemExit("Spec Elicitation Record missing spec_id in front matter.")
ready = data.get("ready_for_planning")
if ready is not True:
    raise SystemExit("Spec Elicitation Record not ready_for_planning=true.")
blocking = data.get("blocking_unknowns")
if not isinstance(blocking, list):
    raise SystemExit("Spec Elicitation Record missing blocking_unknowns list in front matter.")
if blocking:
    raise SystemExit("Spec Elicitation Record has blocking_unknowns; resolve before planning.")
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

# Prompt hygiene: active prompts must be referenced from todo.md; completed prompts must not be referenced.
python - <<'PY' "$TODO_FILE" "$ROOT"
import re
import sys
from pathlib import Path

todo_path = Path(sys.argv[1])
root = Path(sys.argv[2])
prompts_dir = root / "prompts"
if not prompts_dir.is_dir():
    raise SystemExit(0)
if not todo_path.is_file():
    raise SystemExit(f"Todo file not found: {todo_path}")

text = todo_path.read_text(encoding="utf-8")
refs = set(re.findall(r"prompts/[A-Za-z0-9._\\-/]+\\.md", text))
completed = sorted(r for r in refs if r.startswith("prompts/completed/"))
if completed:
    raise SystemExit(f\"todo.md references completed prompts: {', '.join(completed)}\")
missing = sorted(r for r in refs if not (root / r).is_file())
if missing:
    raise SystemExit(f\"todo.md references missing prompts: {', '.join(missing)}\")
allow = {"plan.md", "execute.md", "README.md"}
active = [p for p in prompts_dir.iterdir() if p.is_file() and p.suffix == ".md" and p.name not in allow]
stale = sorted(f"prompts/{p.name}" for p in active if f"prompts/{p.name}" not in refs)
if stale:
    raise SystemExit(f\"Unreferenced prompt artifacts in prompts/: {', '.join(stale)}\")
PY

# Validate Concept Dependency Graph (if validator exists).
if [[ "$MODE" == "execute" && -f "$ROOT/scripts/validate-concept-graph.js" ]]; then
  if ! command -v node >/dev/null 2>&1; then
    echo "Node.js is required to run concept graph validation." >&2
    exit 1
  fi
  (cd "$ROOT" && node scripts/validate-concept-graph.js)
fi


if [[ ! -x "$ROOT/scripts/run-component.sh" ]]; then
  echo "Missing hub helper: $ROOT/scripts/run-component.sh" >&2
  exit 1
fi

PYTHON_BIN=""
if command -v python3 >/dev/null 2>&1; then
  PYTHON_BIN="$(command -v python3)"
elif command -v python >/dev/null 2>&1; then
  PYTHON_BIN="$(command -v python)"
else
  echo "Python interpreter not found (python3/python)." >&2
  exit 1
fi

CONTRACT_CMD=("$PYTHON_BIN" "scripts/validate-governance-contracts.py"
  "--phase" "$PHASE"
  "--agent" "$AGENT"
  "--pattern" "$PATTERN"
)
if [[ -n "$TASK_CLASS" ]]; then
  CONTRACT_CMD+=("--task-class" "$TASK_CLASS")
fi
if [[ -n "$TASK_ID" ]]; then
  CONTRACT_CMD+=("--task-id" "$TASK_ID")
fi
if [[ -n "$EVENTS_FILE" ]]; then
  CONTRACT_CMD+=("--events" "$EVENTS_FILE")
fi

"$ROOT/scripts/run-component.sh" governance-orchestrator "${CONTRACT_CMD[*]}"

LOG_HELPER="$ROOT/scripts/log_event.py"
CMD=("$PYTHON_BIN" "scripts/enforce-lifecycle.py"
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
