#!/usr/bin/env python3
"""Verifier-anchored evidence check (advisory by default)."""

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


def resolve_mode(arg_mode: str | None, objective: Dict[str, Any]) -> str:
    if arg_mode:
        return arg_mode
    policy = objective.get("verifier_evidence_policy")
    if isinstance(policy, dict):
        mode = policy.get("mode")
        if mode in {"advisory", "enforce"}:
            return mode
    return "advisory"


def normalize_path(raw: str) -> Path:
    path = Path(raw)
    if path.is_absolute():
        return path
    return ROOT / path


def check_claims(
    claims: List[Dict[str, Any]],
    evidence_records: List[Dict[str, Any]],
) -> Dict[str, Any]:
    evidence_map: Dict[str, List[Dict[str, Any]]] = {}
    for record in evidence_records:
        claim_id = record.get("claim_id")
        if isinstance(claim_id, str):
            evidence_map.setdefault(claim_id, []).append(record)

    missing: List[str] = []
    failing: List[str] = []
    missing_refs: Dict[str, List[str]] = {}

    for claim in claims:
        claim_id = claim.get("id")
        if not isinstance(claim_id, str) or not claim_id:
            continue
        refs = claim.get("evidence_refs")
        ref_list = refs if isinstance(refs, list) else []
        resolved_missing: List[str] = []
        for ref in ref_list:
            if not isinstance(ref, str):
                continue
            if not normalize_path(ref).exists():
                resolved_missing.append(ref)
        if resolved_missing:
            missing_refs[claim_id] = resolved_missing

        records = evidence_map.get(claim_id, [])
        has_pass = any(rec.get("pass_fail") == "pass" for rec in records)
        has_fail = any(rec.get("pass_fail") == "fail" for rec in records)
        refs_ok = bool(ref_list) and claim_id not in missing_refs

        if has_pass:
            continue
        if has_fail:
            failing.append(claim_id)
            continue
        if refs_ok:
            continue
        missing.append(claim_id)

    return {
        "missing": missing,
        "failing": failing,
        "missing_refs": missing_refs,
    }


def render_human(result: Dict[str, Any]) -> str:
    lines: List[str] = []
    missing = result["missing"]
    failing = result["failing"]
    missing_refs = result["missing_refs"]

    if not missing and not failing and not missing_refs:
        return "Verifier evidence: ok"

    if missing:
        lines.append(f"Missing evidence for claims: {', '.join(missing)}")
    if failing:
        lines.append(f"Failing evidence for claims: {', '.join(failing)}")
    if missing_refs:
        for claim_id, refs in missing_refs.items():
            joined = ", ".join(refs)
            lines.append(f"Missing evidence refs for {claim_id}: {joined}")
    return "\n".join(lines)


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check verifier evidence coverage.")
    parser.add_argument("--objective", default="objective-contract.json")
    parser.add_argument("--evidence", default="artifacts/verifier-evidence.json")
    parser.add_argument("--mode", choices=["advisory", "enforce"], default=None)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    objective_path = normalize_path(args.objective)
    if not objective_path.is_file():
        raise SystemExit(f"Objective Contract not found: {objective_path}")

    objective = load_yaml_or_json(objective_path, "Objective Contract")
    mode = resolve_mode(args.mode, objective)

    claims = objective.get("verifiable_claims")
    if claims is None:
        if args.json:
            print(json.dumps({"mode": mode, "status": "ok", "claims": 0}, indent=2))
        else:
            print("Verifier evidence: no verifiable claims declared")
        return 0

    if not isinstance(claims, list):
        raise SystemExit("Objective Contract verifiable_claims must be a list.")

    evidence_path = normalize_path(args.evidence)
    evidence_records: List[Dict[str, Any]] = []
    if evidence_path.is_file():
        evidence = load_yaml_or_json(evidence_path, "Verifier Evidence")
        records = evidence.get("records")
        if isinstance(records, list):
            evidence_records = records
        else:
            raise SystemExit("Verifier Evidence records must be a list.")

    result = check_claims(claims, evidence_records)
    status = "ok" if not result["missing"] and not result["failing"] and not result["missing_refs"] else "issues"

    if args.json:
        payload = {
            "mode": mode,
            "status": status,
            "claims": len(claims),
            "missing": result["missing"],
            "failing": result["failing"],
            "missing_refs": result["missing_refs"],
        }
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print(render_human(result))

    if mode == "enforce" and status != "ok":
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
