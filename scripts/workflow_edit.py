#!/usr/bin/env python3
"""Helper for editing and validating CERES workflow settings."""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def resolve_path(raw: str) -> Path:
    path = Path(raw)
    if path.is_absolute():
        return path
    return ROOT / path


def ensure_proposed(current_path: Path, proposed_path: Path) -> bool:
    if proposed_path.exists():
        return False
    if not current_path.exists():
        raise SystemExit(f"Current workflow config not found: {current_path}")
    proposed_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(current_path, proposed_path)
    return True


def open_in_editor(path: Path, editor_override: str | None) -> None:
    editor = editor_override or os.environ.get("EDITOR")
    if not editor:
        sys.stderr.write("WARN: EDITOR not set; skipping --open.\n")
        return
    if not sys.stdin.isatty():
        sys.stderr.write("WARN: --open requested without a TTY; skipping.\n")
        return
    subprocess.run([editor, str(path)], check=False)


def run_workflow_guard(
    current_path: Path,
    proposed_path: Path,
    apply: bool,
    confirm: bool,
    fail_on_warning: bool,
    json_output: bool,
) -> int:
    guard = ROOT / "scripts" / "workflow_guard.py"
    if not guard.exists():
        raise SystemExit(f"Workflow guard not found: {guard}")
    cmd = [
        sys.executable,
        str(guard),
        "--current",
        str(current_path),
        "--proposed",
        str(proposed_path),
    ]
    if apply:
        cmd.append("--apply")
    if confirm:
        cmd.append("--confirm")
    if fail_on_warning:
        cmd.append("--fail-on-warning")
    if json_output:
        cmd.append("--json")
    result = subprocess.run(cmd, check=False)
    return result.returncode


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Edit and validate ceres.workflow.yaml safely.")
    parser.add_argument("--current", default="ceres.workflow.yaml")
    parser.add_argument("--proposed", default="ceres.workflow.proposed.yaml")
    parser.add_argument("--open", action="store_true", help="Open the proposed workflow config in $EDITOR.")
    parser.add_argument("--editor", default=None, help="Override $EDITOR for --open.")
    parser.add_argument("--apply", action="store_true", help="Apply proposed workflow via workflow guard.")
    parser.add_argument("--confirm", action="store_true", help="Auto-confirm warnings when applying.")
    parser.add_argument("--fail-on-warning", action="store_true", help="Fail if warnings exist.")
    parser.add_argument("--json", action="store_true", help="Emit workflow guard output as JSON.")
    args = parser.parse_args(argv)

    current_path = resolve_path(args.current)
    proposed_path = resolve_path(args.proposed)

    created = ensure_proposed(current_path, proposed_path)
    if created:
        print(f"Created proposed workflow config: {proposed_path}")

    if args.open:
        open_in_editor(proposed_path, args.editor)

    code = run_workflow_guard(
        current_path=current_path,
        proposed_path=proposed_path,
        apply=args.apply,
        confirm=args.confirm,
        fail_on_warning=args.fail_on_warning,
        json_output=args.json,
    )

    if not args.apply:
        print("Review proposed workflow config and re-run with --apply to commit changes.")

    return code


if __name__ == "__main__":
    raise SystemExit(main())
