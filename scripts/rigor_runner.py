#!/usr/bin/env python3
"""Rigor runner helpers (execution-only; no gating)."""

from __future__ import annotations

import shlex
import subprocess
from pathlib import Path
from typing import Dict, List


def run_command(command: str, args: List[str] | None = None, cwd: Path | None = None) -> Dict:
    cmd = shlex.split(command)
    if args:
        cmd.extend(args)
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=str(cwd) if cwd else None)
    return {
        "command": cmd,
        "exit_code": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
    }


def run_verifiers(verifiers: List[Dict], cwd: Path | None = None) -> List[Dict]:
    results: List[Dict] = []
    for verifier in verifiers:
        output = run_command(verifier["command"], verifier.get("args"), cwd=cwd)
        status = "pass" if output["exit_code"] == 0 else "fail"
        results.append(
            {
                "id": verifier.get("id"),
                "status": status,
                "exit_code": output["exit_code"],
                "stdout": output["stdout"],
                "stderr": output["stderr"],
            }
        )
    return results


def run_oracle(oracle: Dict, cwd: Path | None = None) -> Dict:
    output = run_command(oracle["script"], oracle.get("args"), cwd=cwd)
    return {
        "exit_code": output["exit_code"],
        "stdout": output["stdout"],
        "stderr": output["stderr"],
    }


def run_oracle_and_verify(oracle: Dict, verifiers: List[Dict], cwd: Path | None = None) -> Dict:
    oracle_result = run_oracle(oracle, cwd=cwd)
    verifier_results = run_verifiers(verifiers, cwd=cwd)
    return {
        "oracle": oracle_result,
        "verifiers": verifier_results,
    }


def run_exploit_probe(exploit_probe: Dict, cwd: Path | None = None) -> Dict:
    output = run_command(exploit_probe["script"], exploit_probe.get("args"), cwd=cwd)
    return {
        "status": "flagged",
        "exit_code": output["exit_code"],
        "stdout": output["stdout"],
        "stderr": output["stderr"],
        "flagged": True,
    }
