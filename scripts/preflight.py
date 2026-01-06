#!/usr/bin/env python3
"""CERES preflight fallback.

Mirrors preflight.sh as of 85006775d8fe00470c49804eedede96817fce841.
Fallback only; shell remains authoritative.
"""

import json
import os
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
TASK_ID = ""


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
  --task-id <id>              Optional task identifier for logging
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


def run_or_exit(cmd: list, **kwargs) -> None:
    try:
        result = subprocess.run(cmd, **kwargs)
    except FileNotFoundError:
        sys.stderr.write(f"{cmd[0]}: command not found\n")
        sys.exit(127)
    if result.returncode != 0:
        sys.exit(result.returncode)


def main() -> None:
    global MODE, PROMPT_FILE, REPORT_FILE, TODO_FILE, GAP_LEDGER, OBJECTIVE, TASK_ID

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
        elif arg == "--task-id" and i + 1 < len(args):
            TASK_ID = args[i + 1]
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

    prompt_file = Path(make_abs(PROMPT_FILE))
    report_file = Path(make_abs(REPORT_FILE))
    todo_file = Path(make_abs(TODO_FILE))
    gap_ledger = Path(make_abs(GAP_LEDGER))
    objective = Path(make_abs(OBJECTIVE))

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
