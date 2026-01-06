#!/usr/bin/env python3
"""CERES preflight fallback.

Mirrors preflight.sh.
Fallback only; shell remains authoritative.
"""

import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

MODE = "execute"
PROMPT_FILE = "todo-inbox.md"
REPORT_FILE = str(ROOT / "logs" / "prompt-debug-report.yaml")
TODO_FILE = "todo.md"
GAP_LEDGER = "gap-ledger.json"
OBJECTIVE = "objective-contract.json"
ELICITATION = "specs/elicitation"
TASK_ID = ""
PHASE = ""
AGENT = ""
PATTERN = ""
TASK_CLASS = ""
EVENTS = ""


def usage() -> None:
    print(
        """Usage: ./scripts/preflight.sh [options]

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
"""
    )


def make_abs(value: str) -> str:
    if value.startswith("/"):
        return value
    return str(ROOT / value)


def load_yaml_or_json(path: Path, label: str) -> dict:
    text = path.read_text(encoding="utf-8")
    data = None
    try:
        import yaml  # type: ignore
    except Exception:
        yaml = None

    if yaml is not None:
        try:
            data = yaml.safe_load(text)
        except Exception:
            data = None

    if data is None:
        try:
            data = json.loads(text)
        except Exception as exc:
            raise SystemExit(f"Failed to parse {label}: {exc}")

    return data or {}


def parse_front_matter(text: str) -> dict:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise SystemExit("Spec Elicitation Record missing front matter (expected leading ---).")

    front_matter_lines = []
    end_index = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end_index = i
            break
        front_matter_lines.append(lines[i])

    if end_index is None:
        raise SystemExit("Spec Elicitation Record front matter not terminated (missing ---).")

    data: dict[str, object] = {}
    current_key: str | None = None

    for raw_line in front_matter_lines:
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if re.match(r"^[A-Za-z0-9_\-]+\s*:", line):
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
                items = data.setdefault(current_key, [])
                if isinstance(items, list):
                    items.append(item)
        else:
            continue

    return data


def resolve_elicitation(path: Path) -> Path:
    if path.is_dir():
        candidates = sorted(p for p in path.glob("*.md") if p.is_file())
        if not candidates:
            raise SystemExit(f"Spec Elicitation Record not found in {path}")
        if len(candidates) > 1:
            names = ", ".join(p.name for p in candidates)
            raise SystemExit(
                "Multiple Spec Elicitation Records found. "
                "Provide a single file or set --elicitation <path>. "
                f"Found: {names}"
            )
        return candidates[0]

    if not path.is_file():
        raise SystemExit(f"Spec Elicitation Record not found: {path}")

    return path


def validate_elicitation(path: Path) -> None:
    data = parse_front_matter(path.read_text(encoding="utf-8"))
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


def run_or_exit(cmd: list, **kwargs) -> None:
    try:
        result = subprocess.run(cmd, **kwargs)
    except FileNotFoundError:
        sys.stderr.write(f"{cmd[0]}: command not found\n")
        sys.exit(127)
    if result.returncode != 0:
        sys.exit(result.returncode)


def main() -> None:
    global MODE, PROMPT_FILE, REPORT_FILE, TODO_FILE, GAP_LEDGER, OBJECTIVE, ELICITATION, TASK_ID

    args = sys.argv[1:]
    i = 0
    while i < len(args):
        arg = args[i]
        if arg == "--mode" and i + 1 < len(args):
            MODE = args[i + 1]
            i += 2
        elif arg == "--prompt" and i + 1 < len(args):
            PROMPT_FILE = args[i + 1]
            i += 2
        elif arg == "--prompt-report" and i + 1 < len(args):
            REPORT_FILE = args[i + 1]
            i += 2
        elif arg == "--todo" and i + 1 < len(args):
            TODO_FILE = args[i + 1]
            i += 2
        elif arg == "--gap-ledger" and i + 1 < len(args):
            GAP_LEDGER = args[i + 1]
            i += 2
        elif arg == "--objective" and i + 1 < len(args):
            OBJECTIVE = args[i + 1]
            i += 2
        elif arg == "--elicitation" and i + 1 < len(args):
            ELICITATION = args[i + 1]
            i += 2
        elif arg == "--task-id" and i + 1 < len(args):
            TASK_ID = args[i + 1]
            i += 2
        elif arg == "--phase" and i + 1 < len(args):
            PHASE = args[i + 1]
            i += 2
        elif arg == "--agent" and i + 1 < len(args):
            AGENT = args[i + 1]
            i += 2
        elif arg == "--pattern" and i + 1 < len(args):
            PATTERN = args[i + 1]
            i += 2
        elif arg == "--task-class" and i + 1 < len(args):
            TASK_CLASS = args[i + 1]
            i += 2
        elif arg == "--events" and i + 1 < len(args):
            EVENTS = args[i + 1]
            i += 2
        elif arg in {"-h", "--help"}:
            usage()
            sys.exit(0)
        else:
            sys.stderr.write(f"Unknown option: {arg}\n")
            usage()
            sys.exit(1)

    if MODE not in {"plan", "execute"}:
        sys.stderr.write(f"Invalid mode: {MODE} (expected plan or execute)\n")
        sys.exit(1)

    if not PHASE:
        PHASE = "planning" if MODE == "plan" else "execution"

    if not AGENT:
        AGENT = "Planner" if MODE == "plan" else "Execution"

    if not PATTERN:
        PATTERN = "planning" if MODE == "plan" else "tool-use"

    prompt_file = Path(make_abs(PROMPT_FILE))
    report_file = Path(make_abs(REPORT_FILE))
    todo_file = Path(make_abs(TODO_FILE))
    gap_ledger = Path(make_abs(GAP_LEDGER))
    objective = Path(make_abs(OBJECTIVE))
    elicitation_path = Path(make_abs(ELICITATION))

    events_path = Path(make_abs(EVENTS)) if EVENTS else None

    (ROOT / "logs").mkdir(parents=True, exist_ok=True)

    if not prompt_file.is_file():
        sys.stderr.write(f"Prompt file not found: {prompt_file}\n")
        sys.exit(1)

    report_file.parent.mkdir(parents=True, exist_ok=True)
    with report_file.open("w", encoding="utf-8") as handle:
        run_or_exit([str(ROOT / "prompt-debugger" / "cli.py"), "--prompt-file", str(prompt_file)], stdout=handle)

    report = load_yaml_or_json(report_file, "Prompt Debug Report")
    status = report.get("status")
    if status != "approved":
        raise SystemExit(f"Prompt Debug Report status is '{status}'. Resolve issues before proceeding.")

    if not objective.is_file():
        sys.stderr.write(f"Objective Contract missing: {objective}\n")
        sys.exit(1)

    objective_data = load_yaml_or_json(objective, "Objective Contract")
    status = objective_data.get("status")
    if MODE == "execute" and status != "committed":
        raise SystemExit(
            f"Objective Contract status must be 'committed' for execute mode (found '{status}')."
        )
    if MODE == "plan" and status not in {"draft", "committed"}:
        raise SystemExit(
            f"Objective Contract status must be draft or committed for plan mode (found '{status}')."
        )

    elicitation_file = resolve_elicitation(elicitation_path)
    validate_elicitation(elicitation_file)

    if not gap_ledger.is_file():
        sys.stderr.write(f"Gap Ledger missing: {gap_ledger}\n")
        sys.exit(1)

    gap_data = load_yaml_or_json(gap_ledger, "Gap Ledger")
    gaps = gap_data.get("gaps")
    if not isinstance(gaps, list):
        raise SystemExit("Gap Ledger must contain a 'gaps' list")

    if MODE == "execute":
        blocking = [
            gap
            for gap in gaps
            if isinstance(gap, dict) and gap.get("blocking") is True and gap.get("status") != "resolved"
        ]
        if blocking:
            ids = [gap.get("gap_id", "<unknown>") for gap in blocking]
            raise SystemExit(f"Blocking gaps unresolved: {', '.join(ids)}")

    run_component = ROOT / "scripts" / "run-component.sh"
    if not run_component.exists() or not os.access(run_component, os.X_OK):
        sys.stderr.write(f"Missing hub helper: {run_component}\n")
        sys.exit(1)

    contract_cmd = [
        sys.executable,
        "scripts/validate-governance-contracts.py",
        "--phase",
        PHASE,
        "--agent",
        AGENT,
        "--pattern",
        PATTERN,
    ]
    if TASK_CLASS:
        contract_cmd.extend(["--task-class", TASK_CLASS])
    if TASK_ID:
        contract_cmd.extend(["--task-id", TASK_ID])
    if events_path:
        contract_cmd.extend(["--events", str(events_path)])

    run_or_exit([str(run_component), "governance-orchestrator", " ".join(contract_cmd)], cwd=str(ROOT))

    cmd = [
        "scripts/enforce-lifecycle.py",
        "--todo",
        str(todo_file),
        "--gap-ledger",
        str(gap_ledger),
        "--prompt-report",
        str(report_file),
        "--require-ceres-todo",
        "--require-gap-ledger",
        "--validate-gap-ledger",
        "--require-todo-structure",
        "--log-helper",
        str(ROOT / "scripts" / "log_event.py"),
    ]

    if TASK_ID:
        cmd.extend(["--task-id", TASK_ID])

    run_or_exit([str(run_component), "governance-orchestrator", " ".join(cmd)], cwd=str(ROOT))

    print(f"Preflight checks passed ({MODE} mode).")


if __name__ == "__main__":
    main()
