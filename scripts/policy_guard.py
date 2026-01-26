#!/usr/bin/env python3
"""Policy guard for macro CERES settings (validate, warn, confirm)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

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


def validate_policy(policy: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    version = policy.get("version")
    if not isinstance(version, int) or version < 1:
        errors.append("version must be an integer >= 1")

    policy_block = policy.get("policy")
    if not isinstance(policy_block, dict):
        errors.append("policy block missing or invalid")
        return errors

    def require_enum(key: str, allowed: List[str]) -> None:
        value = policy_block.get(key)
        if value not in allowed:
            errors.append(f"policy.{key} must be one of {allowed}")

    require_enum("rigor_level", ["low", "standard", "high"])
    require_enum("autonomy_level", ["minimal", "constrained", "advanced"])
    require_enum("risk_tolerance", ["low", "medium", "high"])
    require_enum("execution_continuity", ["manual", "auto-safe"])
    require_enum("observability_depth", ["normal", "verbose"])

    return errors


def warn_policy(policy: Dict[str, Any]) -> List[str]:
    warnings: List[str] = []
    block = policy.get("policy", {}) if isinstance(policy.get("policy"), dict) else {}

    rigor = block.get("rigor_level")
    autonomy = block.get("autonomy_level")
    risk = block.get("risk_tolerance")
    continuity = block.get("execution_continuity")
    observability = block.get("observability_depth")

    if autonomy == "advanced" and risk == "low":
        warnings.append("advanced autonomy with low risk tolerance may be contradictory")
    if continuity == "auto-safe" and rigor == "low":
        warnings.append("auto-safe execution with low rigor may be unsafe")
    if observability == "normal" and rigor == "high":
        warnings.append("high rigor with normal observability may reduce auditability")
    if autonomy == "advanced" and continuity != "manual":
        warnings.append("advanced autonomy should remain manual execution continuity")
    if risk == "high" and rigor == "low":
        warnings.append("high risk tolerance with low rigor may increase drift")

    return warnings


def diff_policy(current: Dict[str, Any], proposed: Dict[str, Any]) -> List[str]:
    diffs: List[str] = []
    current_block = current.get("policy", {}) if isinstance(current.get("policy"), dict) else {}
    proposed_block = proposed.get("policy", {}) if isinstance(proposed.get("policy"), dict) else {}

    keys = sorted(set(current_block.keys()) | set(proposed_block.keys()))
    for key in keys:
        if current_block.get(key) != proposed_block.get(key):
            diffs.append(f"policy.{key}: {current_block.get(key)} -> {proposed_block.get(key)}")
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


def apply_policy(proposed_path: Path, current_path: Path) -> None:
    content = proposed_path.read_text(encoding="utf-8")
    current_path.write_text(content, encoding="utf-8")


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Guard macro policy changes with validation and warnings.")
    parser.add_argument("--current", default="ceres.policy.yaml")
    parser.add_argument("--proposed", default=None)
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--confirm", action="store_true")
    parser.add_argument("--fail-on-warning", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    current_path = resolve_path(args.current)
    proposed_path = resolve_path(args.proposed) if args.proposed else current_path

    if not proposed_path.exists():
        raise SystemExit(f"Proposed policy not found: {proposed_path}")

    proposed = load_yaml_or_json(proposed_path, "Proposed policy")
    errors = validate_policy(proposed)
    warnings = warn_policy(proposed)

    diffs: List[str] = []
    if current_path.exists():
        current = load_yaml_or_json(current_path, "Current policy")
        diffs = diff_policy(current, proposed)

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
        apply_policy(proposed_path, current_path)
        print(f"Applied policy to {current_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
