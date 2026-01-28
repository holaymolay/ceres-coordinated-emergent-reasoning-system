#!/usr/bin/env python3
"""Workflow guard for macro CERES workflow settings (validate, warn, confirm)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parent.parent


def load_yaml_or_json(path: Path, label: str) -> Dict[str, Any]:
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

    if not isinstance(data, dict):
        raise SystemExit(f"{label} must be an object.")
    return data


def resolve_path(raw: str) -> Path:
    path = Path(raw)
    if path.is_absolute():
        return path
    return ROOT / path


def validate_workflow(workflow: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    version = workflow.get("version")
    if not isinstance(version, int) or version < 1:
        errors.append("version must be an integer >= 1")

    block = workflow.get("workflow")
    if not isinstance(block, dict):
        errors.append("workflow block missing or invalid")
        return errors

    def require_bool(key: str) -> None:
        value = block.get(key)
        if not isinstance(value, bool):
            errors.append(f"workflow.{key} must be a boolean")

    require_bool("auto_housekeeping")
    require_bool("auto_push")
    require_bool("announce_push")
    return errors


def warn_workflow(workflow: Dict[str, Any]) -> List[str]:
    warnings: List[str] = []
    block = workflow.get("workflow", {}) if isinstance(workflow.get("workflow"), dict) else {}
    auto_housekeeping = block.get("auto_housekeeping")
    auto_push = block.get("auto_push")
    announce_push = block.get("announce_push")

    if auto_housekeeping is False:
        warnings.append("auto_housekeeping disabled; completed tasks may drift without manual sync")
    if auto_push is False and announce_push is True:
        warnings.append("announce_push enabled but auto_push disabled; remember to report manual pushes")
    return warnings


def diff_workflow(current: Dict[str, Any], proposed: Dict[str, Any]) -> List[str]:
    diffs: List[str] = []
    current_block = current.get("workflow", {}) if isinstance(current.get("workflow"), dict) else {}
    proposed_block = proposed.get("workflow", {}) if isinstance(proposed.get("workflow"), dict) else {}

    keys = sorted(set(current_block.keys()) | set(proposed_block.keys()))
    for key in keys:
        if current_block.get(key) != proposed_block.get(key):
            diffs.append(f"workflow.{key}: {current_block.get(key)} -> {proposed_block.get(key)}")
    return diffs


def confirm_if_needed(warnings: List[str], confirm: bool) -> bool:
    if not warnings:
        return True
    if confirm:
        return True
    if not sys.stdin.isatty():
        return False
    print("Warnings detected:")
    for warning in warnings:
        print(f"- {warning}")
    response = input("Proceed with these changes? (yes/no): ").strip().lower()
    return response in {"yes", "y"}


def apply_workflow(proposed_path: Path, current_path: Path) -> None:
    content = proposed_path.read_text(encoding="utf-8")
    current_path.write_text(content, encoding="utf-8")


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Guard macro workflow settings with validation and warnings.")
    parser.add_argument("--current", default="ceres.workflow.yaml")
    parser.add_argument("--proposed", default=None)
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--confirm", action="store_true")
    parser.add_argument("--fail-on-warning", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    current_path = resolve_path(args.current)
    proposed_path = resolve_path(args.proposed) if args.proposed else current_path

    if not proposed_path.exists():
        raise SystemExit(f"Proposed workflow config not found: {proposed_path}")

    proposed = load_yaml_or_json(proposed_path, "Proposed workflow config")
    errors = validate_workflow(proposed)
    warnings = warn_workflow(proposed)

    diffs: List[str] = []
    if current_path.exists():
        current = load_yaml_or_json(current_path, "Current workflow config")
        diffs = diff_workflow(current, proposed)

    if args.json:
        payload = {
            "errors": errors,
            "warnings": warnings,
            "diffs": diffs,
            "apply": args.apply,
        }
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        if diffs:
            print("Proposed changes:")
            for diff in diffs:
                print(f"- {diff}")
        if warnings:
            print("Warnings:")
            for warning in warnings:
                print(f"- {warning}")

    if errors:
        return 1
    if warnings and args.fail_on_warning:
        return 2

    if args.apply:
        if not confirm_if_needed(warnings, args.confirm):
            print("Change not applied.")
            return 3
        apply_workflow(proposed_path, current_path)
        print(f"Applied workflow config to {current_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
