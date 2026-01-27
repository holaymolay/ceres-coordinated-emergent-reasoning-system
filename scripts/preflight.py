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
PROMPT_ALLOWLIST = {"plan.md", "execute.md", "README.md"}
PROMPT_REF_RE = re.compile(r"prompts/[A-Za-z0-9._\\-/]+\\.md")


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


def validate_prompt_hygiene(todo_file: Path) -> None:
    prompts_dir = ROOT / "prompts"
    if not prompts_dir.is_dir():
        return
    if not todo_file.is_file():
        raise SystemExit(f"Todo file not found: {todo_file}")

    text = todo_file.read_text(encoding="utf-8")
    refs = set(PROMPT_REF_RE.findall(text))
    completed_refs = sorted(ref for ref in refs if ref.startswith("prompts/completed/"))
    if completed_refs:
        joined = ", ".join(completed_refs)
        raise SystemExit(f"todo.md references completed prompts: {joined}")

    missing = sorted(ref for ref in refs if not (ROOT / ref).is_file())
    if missing:
        joined = ", ".join(missing)
        raise SystemExit(f"todo.md references missing prompts: {joined}")

    active_files = [
        p
        for p in prompts_dir.iterdir()
        if p.is_file() and p.suffix == ".md" and p.name not in PROMPT_ALLOWLIST
    ]
    stale = sorted(f"prompts/{p.name}" for p in active_files if f"prompts/{p.name}" not in refs)
    if stale:
        joined = ", ".join(stale)
        raise SystemExit(f"Unreferenced prompt artifacts in prompts/: {joined}")


def validate_elicitation(path: Path) -> str:
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

    return spec_id.strip()


def run_or_exit(cmd: list, **kwargs) -> None:
    try:
        result = subprocess.run(cmd, **kwargs)
    except FileNotFoundError:
        sys.stderr.write(f"{cmd[0]}: command not found\n")
        sys.exit(127)
    if result.returncode != 0:
        sys.exit(result.returncode)


def emit_gate_event(
    log_root: Path,
    phase: str,
    agent: str,
    pattern: str,
    task_id: str | None,
    spec_id: str | None,
    status: str,
    message: str,
    context: dict | None,
) -> None:
    if not log_root.exists():
        return
    log_helper = ROOT / "scripts" / "log_event.py"
    if not log_helper.exists():
        return
    cmd = [
        sys.executable,
        str(log_helper),
        "--type",
        "gate",
        "--status",
        status,
        "--message",
        message,
        "--phase",
        phase,
        "--agent",
        agent,
        "--pattern",
        pattern,
    ]
    if task_id:
        cmd.extend(["--task-id", task_id])
    if spec_id:
        cmd.extend(["--spec-id", spec_id])
    if context:
        cmd.extend(["--context", json.dumps(context)])
    subprocess.run(cmd, cwd=str(log_root), check=False)


def policy_guard_advisory(
    log_root: Path,
    phase: str,
    agent: str,
    pattern: str,
    task_id: str | None,
    spec_id: str | None,
) -> None:
    guard = ROOT / "scripts" / "policy_guard.py"
    policy_path = ROOT / "ceres.policy.yaml"
    if not guard.exists():
        return
    if not policy_path.exists():
        sys.stderr.write("WARN: policy guard advisory skipped (missing ceres.policy.yaml).\n")
        emit_gate_event(
            log_root,
            phase,
            agent,
            pattern,
            task_id,
            spec_id,
            "warn",
            "policy guard advisory skipped",
            {"stage": "policy_guard", "reason": "missing_policy"},
        )
        return

    result = subprocess.run(
        [sys.executable, str(guard), "--current", str(policy_path), "--json"],
        capture_output=True,
        text=True,
        cwd=str(ROOT),
    )

    payload = {}
    stdout = (result.stdout or "").strip()
    stderr = (result.stderr or "").strip()
    if stdout:
        try:
            payload = json.loads(stdout)
        except json.JSONDecodeError as exc:
            sys.stderr.write(f"WARN: policy guard advisory parse failed: {exc}\n")
            emit_gate_event(
                log_root,
                phase,
                agent,
                pattern,
                task_id,
                spec_id,
                "warn",
                "policy guard advisory failed",
                {"stage": "policy_guard", "reason": "parse_failed", "error": str(exc)},
            )
            return

    errors = payload.get("errors") if isinstance(payload.get("errors"), list) else []
    warnings = payload.get("warnings") if isinstance(payload.get("warnings"), list) else []

    if errors:
        for error in errors:
            sys.stderr.write(f"WARN: policy guard advisory error: {error}\n")
    if warnings:
        for warning in warnings:
            sys.stderr.write(f"WARN: policy guard advisory warning: {warning}\n")
    if result.returncode != 0 and not errors and not warnings:
        sys.stderr.write(
            f"WARN: policy guard advisory returned exit code {result.returncode}.\n"
        )
    if stderr:
        sys.stderr.write(f"WARN: policy guard advisory stderr: {stderr}\n")

    status = "warn" if errors or warnings or result.returncode != 0 else "info"
    context = {"stage": "policy_guard"}
    if errors:
        context["errors"] = errors
    if warnings:
        context["warnings"] = warnings
    if result.returncode != 0:
        context["exit_code"] = result.returncode
    if stderr:
        context["stderr"] = stderr

    emit_gate_event(
        log_root,
        phase,
        agent,
        pattern,
        task_id,
        spec_id,
        status,
        "policy guard advisory",
        context,
    )


def main() -> None:
    mode = MODE
    prompt_arg = PROMPT_FILE
    report_arg = REPORT_FILE
    todo_arg = TODO_FILE
    gap_ledger_arg = GAP_LEDGER
    objective_arg = OBJECTIVE
    elicitation_arg = ELICITATION
    task_id = TASK_ID
    task_class = TASK_CLASS
    events = EVENTS
    spec_id = ""

    phase = "planning" if mode == "plan" else "execution"
    agent = "Planner" if mode == "plan" else "Execution"
    pattern = "planning" if mode == "plan" else "tool-use"
    phase_set = False
    agent_set = False
    pattern_set = False

    args = sys.argv[1:]
    i = 0
    while i < len(args):
        arg = args[i]
        if arg == "--mode" and i + 1 < len(args):
            mode = args[i + 1]
            if not phase_set:
                phase = "planning" if mode == "plan" else "execution"
            if not agent_set:
                agent = "Planner" if mode == "plan" else "Execution"
            if not pattern_set:
                pattern = "planning" if mode == "plan" else "tool-use"
            i += 2
        elif arg == "--prompt" and i + 1 < len(args):
            prompt_arg = args[i + 1]
            i += 2
        elif arg == "--prompt-report" and i + 1 < len(args):
            report_arg = args[i + 1]
            i += 2
        elif arg == "--todo" and i + 1 < len(args):
            todo_arg = args[i + 1]
            i += 2
        elif arg == "--gap-ledger" and i + 1 < len(args):
            gap_ledger_arg = args[i + 1]
            i += 2
        elif arg == "--objective" and i + 1 < len(args):
            objective_arg = args[i + 1]
            i += 2
        elif arg == "--elicitation" and i + 1 < len(args):
            elicitation_arg = args[i + 1]
            i += 2
        elif arg == "--task-id" and i + 1 < len(args):
            task_id = args[i + 1]
            i += 2
        elif arg == "--phase" and i + 1 < len(args):
            phase = args[i + 1]
            phase_set = True
            i += 2
        elif arg == "--agent" and i + 1 < len(args):
            agent = args[i + 1]
            agent_set = True
            i += 2
        elif arg == "--pattern" and i + 1 < len(args):
            pattern = args[i + 1]
            pattern_set = True
            i += 2
        elif arg == "--task-class" and i + 1 < len(args):
            task_class = args[i + 1]
            i += 2
        elif arg == "--events" and i + 1 < len(args):
            events = args[i + 1]
            i += 2
        elif arg in {"-h", "--help"}:
            usage()
            sys.exit(0)
        else:
            sys.stderr.write(f"Unknown option: {arg}\n")
            usage()
            sys.exit(1)

    if mode not in {"plan", "execute"}:
        sys.stderr.write(f"Invalid mode: {mode} (expected plan or execute)\n")
        sys.exit(1)

    prompt_file = Path(make_abs(prompt_arg))
    report_file = Path(make_abs(report_arg))
    todo_file = Path(make_abs(todo_arg))
    gap_ledger = Path(make_abs(gap_ledger_arg))
    objective = Path(make_abs(objective_arg))
    elicitation_path = Path(make_abs(elicitation_arg))
    events_path = Path(make_abs(events)) if events else None
    log_root = ROOT / "governance-orchestrator"

    (ROOT / "logs").mkdir(parents=True, exist_ok=True)
    policy_guard_advisory(log_root, phase, agent, pattern, task_id, spec_id)

    if not prompt_file.is_file():
        emit_gate_event(
            log_root,
            phase,
            agent,
            pattern,
            task_id,
            spec_id,
            "fail",
            "preflight gate failed",
            {"stage": "prompt", "reason": "missing", "path": str(prompt_file)},
        )
        sys.stderr.write(f"Prompt file not found: {prompt_file}\n")
        sys.exit(1)

    report_file.parent.mkdir(parents=True, exist_ok=True)
    result = subprocess.run(
        [str(ROOT / "prompt-debugger" / "cli.py"), "--prompt-file", str(prompt_file)],
        stdout=report_file.open("w", encoding="utf-8"),
        stderr=subprocess.PIPE,
        text=True,
    )
    if result.returncode != 0:
        context = {"stage": "prompt_report", "reason": "prompt_debugger_failed", "exit_code": result.returncode}
        stderr = (result.stderr or "").strip()
        if stderr:
            context["stderr"] = stderr
        emit_gate_event(
            log_root,
            phase,
            agent,
            pattern,
            task_id,
            spec_id,
            "fail",
            "preflight gate failed",
            context,
        )
        if stderr:
            sys.stderr.write(stderr + "\n")
        sys.exit(result.returncode)

    try:
        report = load_yaml_or_json(report_file, "Prompt Debug Report")
    except SystemExit as exc:
        emit_gate_event(
            log_root,
            phase,
            agent,
            pattern,
            task_id,
            spec_id,
            "fail",
            "preflight gate failed",
            {"stage": "prompt_report", "reason": "parse_failed", "error": str(exc)},
        )
        raise

    status = report.get("status")
    if status != "approved":
        emit_gate_event(
            log_root,
            phase,
            agent,
            pattern,
            task_id,
            spec_id,
            "fail",
            "preflight gate failed",
            {"stage": "prompt_report", "reason": "not_approved", "status": status},
        )
        raise SystemExit(f"Prompt Debug Report status is '{status}'. Resolve issues before proceeding.")

    if not objective.is_file():
        emit_gate_event(
            log_root,
            phase,
            agent,
            pattern,
            task_id,
            spec_id,
            "fail",
            "preflight gate failed",
            {"stage": "objective", "reason": "missing", "path": str(objective)},
        )
        sys.stderr.write(f"Objective Contract missing: {objective}\n")
        sys.exit(1)

    try:
        objective_data = load_yaml_or_json(objective, "Objective Contract")
    except SystemExit as exc:
        emit_gate_event(
            log_root,
            phase,
            agent,
            pattern,
            task_id,
            spec_id,
            "fail",
            "preflight gate failed",
            {"stage": "objective", "reason": "parse_failed", "error": str(exc)},
        )
        raise

    status = objective_data.get("status")
    if mode == "execute" and status != "committed":
        emit_gate_event(
            log_root,
            phase,
            agent,
            pattern,
            task_id,
            spec_id,
            "fail",
            "preflight gate failed",
            {"stage": "objective", "reason": "status_invalid", "status": status},
        )
        raise SystemExit(
            f"Objective Contract status must be 'committed' for execute mode (found '{status}')."
        )
    if mode == "plan" and status not in {"draft", "committed"}:
        emit_gate_event(
            log_root,
            phase,
            agent,
            pattern,
            task_id,
            spec_id,
            "fail",
            "preflight gate failed",
            {"stage": "objective", "reason": "status_invalid", "status": status},
        )
        raise SystemExit(
            f"Objective Contract status must be draft or committed for plan mode (found '{status}')."
        )

    try:
        elicitation_file = resolve_elicitation(elicitation_path)
    except SystemExit as exc:
        emit_gate_event(
            log_root,
            phase,
            agent,
            pattern,
            task_id,
            spec_id,
            "fail",
            "preflight gate failed",
            {"stage": "elicitation", "reason": "missing", "error": str(exc), "path": str(elicitation_path)},
        )
        raise

    try:
        spec_id = validate_elicitation(elicitation_file)
    except SystemExit as exc:
        emit_gate_event(
            log_root,
            phase,
            agent,
            pattern,
            task_id,
            spec_id,
            "fail",
            "preflight gate failed",
            {"stage": "elicitation", "reason": "not_ready", "error": str(exc), "path": str(elicitation_file)},
        )
        raise

    if not gap_ledger.is_file():
        emit_gate_event(
            log_root,
            phase,
            agent,
            pattern,
            task_id,
            spec_id,
            "fail",
            "preflight gate failed",
            {"stage": "gap_ledger", "reason": "missing", "path": str(gap_ledger)},
        )
        sys.stderr.write(f"Gap Ledger missing: {gap_ledger}\n")
        sys.exit(1)

    try:
        gap_data = load_yaml_or_json(gap_ledger, "Gap Ledger")
    except SystemExit as exc:
        emit_gate_event(
            log_root,
            phase,
            agent,
            pattern,
            task_id,
            spec_id,
            "fail",
            "preflight gate failed",
            {"stage": "gap_ledger", "reason": "parse_failed", "error": str(exc)},
        )
        raise

    gaps = gap_data.get("gaps")
    if not isinstance(gaps, list):
        emit_gate_event(
            log_root,
            phase,
            agent,
            pattern,
            task_id,
            spec_id,
            "fail",
            "preflight gate failed",
            {"stage": "gap_ledger", "reason": "invalid"},
        )
        raise SystemExit("Gap Ledger must contain a 'gaps' list")

    if mode == "execute":
        blocking = [
            gap
            for gap in gaps
            if isinstance(gap, dict) and gap.get("blocking") is True and gap.get("status") != "resolved"
        ]
        if blocking:
            ids = [gap.get("gap_id", "<unknown>") for gap in blocking]
            emit_gate_event(
                log_root,
                phase,
                agent,
                pattern,
                task_id,
                spec_id,
                "fail",
                "preflight gate failed",
                {"stage": "gap_ledger", "reason": "blocking_unresolved", "gap_ids": ids},
            )
            raise SystemExit(f"Blocking gaps unresolved: {', '.join(ids)}")

    try:
        validate_prompt_hygiene(todo_file)
    except SystemExit as exc:
        emit_gate_event(
            log_root,
            phase,
            agent,
            pattern,
            task_id,
            spec_id,
            "fail",
            "preflight gate failed",
            {"stage": "prompt_hygiene", "reason": "invalid", "error": str(exc)},
        )
        raise

    run_component = ROOT / "scripts" / "run-component.sh"
    if not run_component.exists() or not os.access(run_component, os.X_OK):
        emit_gate_event(
            log_root,
            phase,
            agent,
            pattern,
            task_id,
            spec_id,
            "fail",
            "preflight gate failed",
            {"stage": "runtime", "reason": "run-component-missing", "path": str(run_component)},
        )
        sys.stderr.write(f"Missing hub helper: {run_component}\n")
        sys.exit(1)

    contract_cmd = [
        sys.executable,
        "scripts/validate-governance-contracts.py",
        "--phase",
        phase,
        "--agent",
        agent,
        "--pattern",
        pattern,
    ]
    if task_class:
        contract_cmd.extend(["--task-class", task_class])
    if task_id:
        contract_cmd.extend(["--task-id", task_id])
    if events_path:
        contract_cmd.extend(["--events", str(events_path)])

    contract_result = subprocess.run(
        [str(run_component), "governance-orchestrator", " ".join(contract_cmd)],
        capture_output=True,
        text=True,
        cwd=str(ROOT),
    )
    if contract_result.returncode != 0:
        context = {"stage": "contracts", "reason": "validation_failed", "exit_code": contract_result.returncode}
        stderr = (contract_result.stderr or "").strip()
        stdout = (contract_result.stdout or "").strip()
        if stderr:
            context["stderr"] = stderr
        if stdout:
            context["stdout"] = stdout
        emit_gate_event(
            log_root,
            phase,
            agent,
            pattern,
            task_id,
            spec_id,
            "fail",
            "preflight gate failed",
            context,
        )
        if stderr:
            sys.stderr.write(stderr + "\n")
        elif stdout:
            sys.stderr.write(stdout + "\n")
        sys.exit(contract_result.returncode)

    cmd = [
        sys.executable,
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

    if task_id:
        cmd.extend(["--task-id", task_id])

    run_or_exit([str(run_component), "governance-orchestrator", " ".join(cmd)], cwd=str(ROOT))

    print(f"Preflight checks passed ({mode} mode).")

if __name__ == "__main__":
    main()
