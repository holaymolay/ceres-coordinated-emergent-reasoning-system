#!/usr/bin/env python3
"""Prompt Debugger CLI for CERES.

Reads a prompt from stdin or a file and emits a debug report (YAML if available,
otherwise JSON). This is the pre-governance gate for task-inbox/chat input.
"""
import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict

try:
    import yaml  # type: ignore
except ImportError:  # pragma: no cover - optional dependency
    yaml = None

SCRIPT_DIR = Path(__file__).parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from classify import classify
from validate import validate
from risk_assess import assess
from decision_engine import decide
from debug_report import build


def load_prompt(args: argparse.Namespace) -> str:
    if args.prompt_file:
        return Path(args.prompt_file).read_text()
    if not sys.stdin.isatty():
        return sys.stdin.read()
    raise SystemExit("No prompt provided. Pass --prompt-file or pipe input.")


def emit(report: Dict[str, Any]) -> None:
    if yaml:
        sys.stdout.write(yaml.safe_dump(report, sort_keys=False))
    else:
        sys.stdout.write(json.dumps(report, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser(description="CERES Prompt Debugger")
    parser.add_argument("--prompt-file", help="Path to prompt text (optional)")
    args = parser.parse_args()

    prompt = load_prompt(args)
    classification = classify(prompt)
    issues = validate(prompt)
    risk_level = assess(prompt, issues, classification["destructive"])
    status, suggested = decide(issues, classification["destructive"])
    report = build(
        prompt=prompt,
        detected_intent=classification["detected_intent"],
        repos=classification["repos"],
        risk_level=risk_level,
        issues=issues,
        status=status,
        suggested=suggested,
    )
    emit(report)


if __name__ == "__main__":
    main()
