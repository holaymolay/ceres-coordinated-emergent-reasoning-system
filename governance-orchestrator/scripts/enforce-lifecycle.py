#!/usr/bin/env python3
"""Lifecycle gate checks for CERES governance orchestrator.

Enforces:
- todo.md has unchecked tasks
- optional Gap Ledger presence and validation
- optional Prompt Debug Report presence
- optional CERES todo template check
- optional logging via hub scripts/log_event.py
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Dict, List

MAX_TODO_LINE_LENGTH = 240
EXECUTE_PROMPT_PATTERN = re.compile(r"Execute prompt:\s*([^\s]+)")
FROM_PROMPT_PATTERN = re.compile(r"From prompt\s+([^\s:]+)(?:\s*:\s*(.+))?")

SPEC_ID_MISSING_MESSAGE = (
    "Planning blocked: spec_id not allocated. Run allocate-spec-id.py after elicitation readiness."
)
SPEC_ID_MULTIPLE_MESSAGE = "Planning blocked: multiple spec_id values detected in objective-contract.json."




def has_unchecked_tasks(todo_path: Path) -> bool:
    if not todo_path.exists():
        return False
    return any(line.strip().startswith("- [ ]") for line in todo_path.read_text().splitlines())


def check_ceres_todo(todo_path: Path) -> bool:
    lines = todo_path.read_text().splitlines() if todo_path.exists() else []
    return bool(lines and "CERES" in lines[0])


def log_event(log_helper: Path, status: str, message: str, context: Dict) -> None:
    if not log_helper:
        return
    if not log_helper.exists():
        sys.stderr.write(f"Log helper not found at {log_helper}\n")
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
        "--context",
        json.dumps(context),
    ]
    subprocess.run(cmd, check=False)


def validate_gap_ledger(path: Path) -> str:
    """Call local validate-gap-ledger.py if present; return warning text or ''."""
    validator = path.parent / "validate-gap-ledger.py"
    if not validator.exists():
        return ""
    result = subprocess.run([sys.executable, str(validator), str(path)], capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "Gap ledger validation failed")
    return result.stderr.strip()  # warnings, if any


def is_prompt_path(value: str) -> bool:
    return value.startswith("prompts/prompt-") and value.endswith(".md")


def read_prompt_classification(path: Path) -> str | None:
    classification = None
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("Classification:"):
            classification = line.split(":", 1)[1].strip().lower()
            break
    if classification in {"atomic", "decomposable"}:
        return classification
    return None




def validate_spec_id(objective_path: Path) -> List[str]:
    failures: List[str] = []
    if not objective_path.exists():
        failures.append(SPEC_ID_MISSING_MESSAGE)
        return failures

    try:
        data = json.loads(objective_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        failures.append(SPEC_ID_MISSING_MESSAGE)
        return failures

    spec_id = data.get("spec_id")
    if isinstance(spec_id, list):
        values = [str(value).strip() for value in spec_id if str(value).strip()]
        if len(values) > 1:
            failures.append(SPEC_ID_MULTIPLE_MESSAGE)
            return failures
        if len(values) == 1:
            spec_id = values[0]
        else:
            failures.append(SPEC_ID_MISSING_MESSAGE)
            return failures

    if not isinstance(spec_id, str) or not spec_id.strip():
        failures.append(SPEC_ID_MISSING_MESSAGE)
        return failures

    if ',' in spec_id or ' ' in spec_id.strip():
        failures.append(SPEC_ID_MULTIPLE_MESSAGE)

    return failures

def outcome_from_next_line(lines: List[str], index: int) -> bool:
    if index + 1 >= len(lines):
        return False
    next_line = lines[index + 1].strip()
    if not next_line.lower().startswith("outcome:"):
        return False
    return bool(next_line.split(":", 1)[1].strip())


def validate_prompt_artifacts(todo_path: Path) -> List[str]:
    failures: List[str] = []
    if not todo_path.exists():
        return failures

    lines = todo_path.read_text(encoding="utf-8").splitlines()
    for idx, line in enumerate(lines, start=1):
        if len(line) > MAX_TODO_LINE_LENGTH:
            failures.append(
                f"todo.md line {idx} exceeds {MAX_TODO_LINE_LENGTH} chars; long prompts must be externalized"
            )

    references: List[dict] = []
    for idx, line in enumerate(lines, start=1):
        stripped = line.strip()
        if not stripped.startswith("- ["):
            continue

        if "Execute prompt:" in stripped:
            match = EXECUTE_PROMPT_PATTERN.search(stripped)
            if not match:
                failures.append(f"todo.md line {idx} has Execute prompt without a path")
            else:
                path_value = match.group(1)
                if not is_prompt_path(path_value):
                    failures.append(f"todo.md line {idx} must reference prompts/prompt-*.md")
                tail = stripped[match.end():].strip()
                references.append(
                    {
                        "line": idx,
                        "path": path_value,
                        "outcome": bool(tail) or outcome_from_next_line(lines, idx - 1),
                    }
                )

        if "From prompt" in stripped:
            match = FROM_PROMPT_PATTERN.search(stripped)
            if not match:
                failures.append(f"todo.md line {idx} has From prompt without a path")
            else:
                path_value = match.group(1)
                if not is_prompt_path(path_value):
                    failures.append(f"todo.md line {idx} must reference prompts/prompt-*.md")
                outcome_inline = bool(match.group(2) and match.group(2).strip())
                references.append(
                    {
                        "line": idx,
                        "path": path_value,
                        "outcome": outcome_inline or outcome_from_next_line(lines, idx - 1),
                    }
                )

    grouped: dict[str, list[dict]] = {}
    for ref in references:
        path_value = ref.get("path")
        if not path_value:
            continue
        grouped.setdefault(path_value, []).append(ref)

    hub_root = todo_path.resolve().parent
    for path_value, refs in grouped.items():
        prompt_path = (hub_root / path_value).resolve()
        if not prompt_path.exists():
            failures.append(f"Prompt file not found: {path_value}")
            continue
        classification = read_prompt_classification(prompt_path)
        if not classification:
            failures.append(f"Prompt file missing Classification (atomic|decomposable): {path_value}")
            continue
        if classification == "atomic" and len(refs) != 1:
            failures.append(
                f"Prompt {path_value} is atomic but referenced by {len(refs)} todo entries"
            )
        if classification == "decomposable":
            for ref in refs:
                if not ref.get("outcome"):
                    failures.append(
                        f"Prompt {path_value} is decomposable; todo line {ref['line']} must include an outcome"
                    )

    return failures


def main() -> None:
    parser = argparse.ArgumentParser(description="CERES lifecycle gate")
    parser.add_argument("--todo", type=Path, default=Path("todo.md"), help="Path to todo.md")
    parser.add_argument("--gap-ledger", type=Path, help="Optional path to gap ledger file")
    parser.add_argument("--prompt-report", type=Path, help="Optional path to prompt debug report")
    parser.add_argument("--require-ceres-todo", action="store_true", help="Fail if todo.md does not look like CERES template")
    parser.add_argument("--require-gap-ledger", action="store_true", help="Fail if gap ledger is missing or empty")
    parser.add_argument("--validate-gap-ledger", action="store_true", help="Validate gap ledger content (evidence for resolved gaps)")
    parser.add_argument("--require-todo-structure", action="store_true", help="Fail if todo.md missing required CERES sections")
    parser.add_argument("--task-id", help="Optional task identifier for logging context")
    parser.add_argument("--log-helper", type=Path, help="Optional path to umbrella scripts/log_event.py to log gate outcome")
    args = parser.parse_args()

    failures = []
    warnings = []
    context = {
        "todo": str(args.todo),
        "gap_ledger": str(args.gap_ledger) if args.gap_ledger else None,
        "prompt_report": str(args.prompt_report) if args.prompt_report else None,
        "task_id": args.task_id,
    }

    objective_path = args.todo.resolve().parent / "objective-contract.json"
    context["objective_contract"] = str(objective_path)
    failures.extend(validate_spec_id(objective_path))

    if not has_unchecked_tasks(args.todo):
        failures.append(f"Missing or empty task plan: {args.todo}")

    if args.gap_ledger and not args.gap_ledger.exists():
        failures.append(f"Gap ledger missing: {args.gap_ledger}")

    if args.require_gap_ledger:
        if not args.gap_ledger:
            failures.append("Gap ledger path not provided while --require-gap-ledger is set")
        else:
            if not args.gap_ledger.exists():
                failures.append(f"Gap ledger missing: {args.gap_ledger}")
            elif not args.gap_ledger.read_text().strip():
                failures.append(f"Gap ledger is empty: {args.gap_ledger}")

    if args.validate_gap_ledger and args.gap_ledger and args.gap_ledger.exists():
        try:
            warning_text = validate_gap_ledger(args.gap_ledger)
            if warning_text:
                warnings.append(warning_text)
        except RuntimeError as exc:
            failures.append(str(exc))

    if args.prompt_report and not args.prompt_report.exists():
        failures.append(f"Prompt debug report missing: {args.prompt_report}")

    if args.require_ceres_todo and not check_ceres_todo(args.todo):
        failures.append(f"todo.md does not appear to be the CERES template: {args.todo}")

    if args.require_todo_structure:
        required_sections = ["## Bugs", "## Workflow Governance", "## Current Focus", "## Next Features & Updates", "## Backlog"]
        contents = args.todo.read_text().splitlines() if args.todo.exists() else []
        for section in required_sections:
            if not any(line.strip() == section for line in contents):
                failures.append(f"todo.md missing required section: {section}")

    failures.extend(validate_prompt_artifacts(args.todo))

    if failures:
        sys.stderr.write("Lifecycle gate failed:\n" + "\n".join(f"- {f}" for f in failures) + "\n")
        log_event(args.log_helper, "fail", "lifecycle gate failed", {**context, "failures": failures})
        sys.exit(1)

    if warnings:
        sys.stderr.write("Lifecycle gate warnings:\n" + "\n".join(warnings) + "\n")

    sys.stdout.write("Lifecycle gate passed\n")
    log_event(args.log_helper, "pass", "lifecycle gate passed", context)


if __name__ == "__main__":
    main()
