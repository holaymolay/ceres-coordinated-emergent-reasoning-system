#!/usr/bin/env python3
"""Rigor CLI entrypoints (default-off, opt-in)."""

from __future__ import annotations

import argparse
import json
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

from scripts import rigor_rules, rigor_runner

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


def load_list(path: Path) -> List[str]:
    text = path.read_text(encoding="utf-8").strip()
    if not text:
        return []
    try:
        data = json.loads(text)
    except Exception:
        data = None
    if isinstance(data, list) and all(isinstance(item, str) for item in data):
        return data
    return [line.strip() for line in text.splitlines() if line.strip()]


def emit_event(status: str, message: str, context: Dict[str, Any]) -> None:
    helper = ROOT / "scripts" / "log_event.py"
    if not helper.exists():
        return
    cmd = [
        sys.executable,
        str(helper),
        "--type",
        "rigor",
        "--status",
        status,
        "--message",
        message,
        "--context",
        json.dumps(context),
    ]
    try:
        import subprocess

        subprocess.run(cmd, check=False, cwd=str(ROOT))
    except Exception:
        return


def write_report(report: Dict[str, Any], out_path: Path | None) -> None:
    payload = json.dumps(report, indent=2, sort_keys=True)
    if out_path:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(payload + "\n", encoding="utf-8")
    else:
        print(payload)


def build_report(kind: str, data: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "run_id": str(uuid.uuid4()),
        "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "type": kind,
        "data": data,
    }


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Rigor CLI (default-off).")
    sub = parser.add_subparsers(dest="command", required=True)

    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--rigor", default="rigor.json", help="Path to rigor config.")
    common.add_argument("--out", default=None, help="Write JSON report to path (default: stdout).")

    verify = sub.add_parser("verify", parents=[common], help="Run verifiers and report pass/fail.")
    check_map = sub.add_parser("check-spec-map", parents=[common], help="Check spec<->verifier mapping.")
    check_map.add_argument("--spec-clauses", required=True, help="Path to spec clause list (JSON array or lines).")

    run_oracle = sub.add_parser("run-oracle", parents=[common], help="Run oracle then verifiers.")

    exploit = sub.add_parser("exploit-probe", parents=[common], help="Run exploit probe (always flagged).")

    nondet = sub.add_parser("nondeterminism-report", parents=[common], help="Validate nondeterminism manifest.")
    nondet.add_argument("--task-meta", required=True, help="Path to task metadata (JSON/YAML).")

    args = parser.parse_args(argv)

    rigor_path = Path(args.rigor)
    if not rigor_path.is_absolute():
        rigor_path = ROOT / rigor_path
    if not rigor_path.exists():
        raise SystemExit(f"Rigor config not found: {rigor_path}")
    rigor = load_yaml_or_json(rigor_path, "Rigor config")

    errors = rigor_rules.validate_rigor_block(rigor)
    if errors:
        for err in errors:
            sys.stderr.write(f"ERROR: {err}\n")
        emit_event("fail", "rigor config invalid", {"errors": errors})
        return 1

    out_path = Path(args.out) if args.out else None
    if out_path and not out_path.is_absolute():
        out_path = ROOT / out_path

    if args.command == "verify":
        verifiers = rigor.get("verifiers", [])
        results = rigor_runner.run_verifiers(verifiers, cwd=rigor_path.parent)
        data = {"verifiers": results}
        report = build_report("verify", data)
        emit_event("pass", "rigor verify complete", {"verifiers": results})
        write_report(report, out_path)
        return 0 if all(r["status"] == "pass" for r in results) else 1

    if args.command == "check-spec-map":
        spec_clauses = load_list(Path(args.spec_clauses))
        verifier_ids = [v.get("id") for v in rigor.get("verifiers", []) if isinstance(v, dict)]
        spec_map = rigor.get("spec_map", [])
        errors = rigor_rules.validate_spec_map(spec_clauses, verifier_ids, spec_map)
        data = {"errors": errors, "spec_clauses": spec_clauses, "verifiers": verifier_ids}
        report = build_report("check-spec-map", data)
        status = "pass" if not errors else "fail"
        emit_event(status, "rigor spec map check", data)
        write_report(report, out_path)
        return 0 if not errors else 1

    if args.command == "run-oracle":
        oracle = rigor.get("oracle")
        if not isinstance(oracle, dict):
            raise SystemExit("Rigor config missing oracle block.")
        verifiers = rigor.get("verifiers", [])
        result = rigor_runner.run_oracle_and_verify(oracle, verifiers, cwd=rigor_path.parent)
        report = build_report("run-oracle", result)
        status = "pass" if all(r["status"] == "pass" for r in result["verifiers"]) else "fail"
        emit_event(status, "rigor oracle run", result)
        write_report(report, out_path)
        return 0 if status == "pass" else 1

    if args.command == "exploit-probe":
        exploit_probe = rigor.get("exploit_probe")
        if not isinstance(exploit_probe, dict):
            raise SystemExit("Rigor config missing exploit_probe block.")
        result = rigor_runner.run_exploit_probe(exploit_probe, cwd=rigor_path.parent)
        report = build_report("exploit-probe", result)
        emit_event("warn", "rigor exploit probe flagged", result)
        write_report(report, out_path)
        return 0

    if args.command == "nondeterminism-report":
        task_meta = load_yaml_or_json(Path(args.task_meta), "Task metadata")
        errors = rigor_rules.require_nondeterminism_manifest(task_meta, rigor.get("nondeterminism"))
        data = {"errors": errors}
        report = build_report("nondeterminism-report", data)
        status = "pass" if not errors else "fail"
        emit_event(status, "rigor nondeterminism report", data)
        write_report(report, out_path)
        return 0 if not errors else 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
