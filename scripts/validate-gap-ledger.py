#!/usr/bin/env python3
"""Validate a Gap Ledger for CERES inference enforcement."""
import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

try:
    import yaml  # type: ignore
except ImportError:  # pragma: no cover
    yaml = None

REQUIRED = {"gap_id", "type", "blocking", "answerable_by_system", "resolution_method", "status"}

class ValidationError(Exception):
    pass

def load(path: Path) -> Dict[str, Any]:
    text = path.read_text()
    if path.suffix.lower() in {".yaml", ".yml"}:
        if not yaml:
            raise ValidationError("PyYAML not installed; cannot parse YAML")
        return yaml.safe_load(text)
    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValidationError(f"Invalid JSON: {exc}")

def validate_gap(gap: Dict[str, Any]) -> None:
    missing = REQUIRED - set(gap.keys())
    if missing:
        raise ValidationError(f"Gap {gap.get('gap_id','<unknown>')} missing fields: {', '.join(sorted(missing))}")
    if gap.get("status") == "resolved":
        evidence = gap.get("evidence_links") or []
        assumption = gap.get("assumption", {})
        assumption_text = assumption.get("text") if isinstance(assumption, dict) else None
        if not evidence and not assumption_text:
            raise ValidationError(f"Gap {gap.get('gap_id','<unknown>')} is resolved but has no evidence or assumption recorded")

def validate(doc: Dict[str, Any]) -> List[str]:
    gaps = doc.get("gaps")
    if not isinstance(gaps, list):
        raise ValidationError("Gap ledger must contain a 'gaps' array")
    warnings: List[str] = []
    for gap in gaps:
        if not isinstance(gap, dict):
            raise ValidationError("Each gap must be an object")
        validate_gap(gap)
        if gap.get("status") != "resolved" and gap.get("blocking") is True:
            warnings.append(f"Gap {gap.get('gap_id','<unknown>')} is blocking and unresolved")
    return warnings

def main() -> None:
    parser = argparse.ArgumentParser(description="Validate CERES gap ledger")
    parser.add_argument("path", type=Path, help="Path to gap ledger (JSON/YAML)")
    args = parser.parse_args()

    if not args.path.exists():
        sys.stderr.write(f"Gap ledger not found: {args.path}\n")
        sys.exit(1)

    try:
        doc = load(args.path)
        warnings = validate(doc)
    except ValidationError as exc:
        sys.stderr.write(f"Validation failed: {exc}\n")
        sys.exit(1)

    if warnings:
        sys.stderr.write("Warnings:\n" + "\n".join(f"- {w}" for w in warnings) + "\n")
    else:
        sys.stdout.write("Gap ledger valid\n")

if __name__ == "__main__":
    main()
