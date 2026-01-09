#!/usr/bin/env python3
"""
CERES doctor (read-only, non-authoritative).

Checks:
- Workspace detection (.ceres/workspace or legacy root)
- core.lock integrity vs core submodule (if present)
- Wrapper parity (wrappers executable + underlying scripts present)
- Feature flags (read-only; e.g., pattern recall)
- Removal-proof invariant (legacy fallback exists)

Outputs:
- Human-readable report to stdout
- Optional JSON (--json)
- Optional Signals emission (--emit-signals) as informational notices

No fixes, no gating; exit code is 0 unless tool error occurs.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import subprocess
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

try:
    from observability import signals as signals_module
except Exception:
    signals_module = None


DEFAULT_WRAPPERS = ("preflight", "start-session", "export-handover")
DEFAULT_ROOT = Path(".")


def subprocess_run(cmd: List[str], cwd: Optional[Path] = None) -> str:
    result = subprocess.run(
        cmd,
        cwd=str(cwd) if cwd else None,
        capture_output=True,
        text=True,
        check=False,
    )
    return result.stdout.strip()


@dataclass
class Finding:
    id: str
    status: str  # ok|warning|error
    message: str
    evidence: Dict[str, Any]
    source: str = "doctor"

    def to_signal(self) -> Dict[str, Any]:
        severity = "info" if self.status == "ok" else ("warning" if self.status == "warning" else "critical")
        return {
            "id": self.id,
            "severity": severity,
            "source": self.source,
            "message": self.message,
            "constitutional_reference": "",
        }


def resolve_workspace(env: Optional[Dict[str, str]] = None) -> Tuple[Path, bool]:
    env = env or os.environ
    if "CERES_WORKSPACE" in env:
        path = Path(env["CERES_WORKSPACE"])
    else:
        path = Path(".ceres/workspace")
    return path, path.exists()


def check_workspace(env: Optional[Dict[str, str]] = None) -> Finding:
    path, exists = resolve_workspace(env)
    if exists:
        return Finding(
            id="workspace_detected",
            status="ok",
            message=f"Workspace detected at {path}",
            evidence={"workspace": str(path)},
        )
    return Finding(
        id="workspace_missing",
        status="warning",
        message="Workspace not detected; legacy root in use.",
        evidence={"workspace": str(path)},
    )


def check_core_lock(root: Path, env: Optional[Dict[str, str]] = None) -> Finding:
    env = env or os.environ
    core_dir = Path(env.get("CERES_HOME", root / ".ceres")) / "core"
    lock_path = Path(env.get("CERES_HOME", root / ".ceres")) / "core.lock"

    if not core_dir.exists() or not (core_dir / ".git").exists():
        return Finding(
            id="core_absent",
            status="warning",
            message="Core submodule not present; skipping pin check.",
            evidence={"core_dir": str(core_dir)},
        )
    if not lock_path.exists():
        return Finding(
            id="core_lock_missing",
            status="warning",
            message="core.lock missing; cannot verify pin.",
            evidence={"core_dir": str(core_dir)},
        )
    try:
        proc = subprocess_run(["git", "rev-parse", "HEAD"], cwd=core_dir)
        current_commit = proc.strip()
    except Exception:
        current_commit = ""

    lock_commit = ""
    lock_ref = ""
    lock_remote = ""
    for line in lock_path.read_text(encoding="utf-8").splitlines():
        if line.startswith("commit:"):
            lock_commit = line.split(":", 1)[1].strip()
        elif line.startswith("ref:"):
            lock_ref = line.split(":", 1)[1].strip()
        elif line.startswith("remote:"):
            lock_remote = line.split(":", 1)[1].strip()

    if not current_commit or not lock_commit:
        return Finding(
            id="core_lock_inconclusive",
            status="warning",
            message="Could not determine core commit; verify manually.",
            evidence={"core_dir": str(core_dir), "lock_commit": lock_commit, "current_commit": current_commit},
        )

    if lock_commit != current_commit:
        return Finding(
            id="core_pin_mismatch",
            status="error",
            message="core.lock does not match core submodule commit.",
            evidence={"lock_commit": lock_commit, "current_commit": current_commit, "ref": lock_ref, "remote": lock_remote},
        )

    return Finding(
        id="core_pin_ok",
        status="ok",
        message="core.lock matches core submodule commit.",
        evidence={"lock_commit": lock_commit, "ref": lock_ref, "remote": lock_remote},
    )


def check_wrappers(root: Path) -> Finding:
    missing: List[str] = []
    for name in DEFAULT_WRAPPERS:
        wrapper = root / ".ceres" / "bin" / name
        if not wrapper.exists() or not os.access(wrapper, os.X_OK):
            missing.append(str(wrapper))
    if missing:
        return Finding(
            id="wrapper_missing",
            status="warning",
            message="One or more wrappers missing or not executable.",
            evidence={"missing": missing},
        )
    return Finding(
        id="wrapper_parity_ok",
        status="ok",
        message="Wrappers present and executable.",
        evidence={"checked": list(DEFAULT_WRAPPERS)},
    )


def check_removal_invariant(root: Path) -> Finding:
    legacy_scripts = [root / "scripts" / "preflight.sh"]
    missing = [str(p) for p in legacy_scripts if not p.exists()]
    if missing:
        return Finding(
            id="legacy_fallback_missing",
            status="warning",
            message="Legacy fallback scripts missing; removal-proof invariant weakened.",
            evidence={"missing": missing},
        )
    return Finding(
        id="removal_proof_ok",
        status="ok",
        message="Legacy fallback scripts present; removal-proof invariant holds.",
        evidence={"legacy_scripts": [str(p) for p in legacy_scripts]},
    )


def check_feature_flags(env: Optional[Dict[str, str]] = None) -> Finding:
    env = env or os.environ
    pattern_recall_enabled = env.get("PATTERN_RECALL_ENABLED", "").lower() in {"1", "true", "yes", "on"}
    flags = {"pattern_recall_enabled": pattern_recall_enabled}
    return Finding(
        id="feature_flags",
        status="ok",
        message="Feature flags captured (informational).",
        evidence=flags,
    )


def run_checks(root: Path, env: Optional[Dict[str, str]] = None) -> List[Finding]:
    return [
        check_workspace(env),
        check_core_lock(root, env),
        check_wrappers(root),
        check_removal_invariant(root),
        check_feature_flags(env),
    ]


def render_human(findings: List[Finding]) -> str:
    lines: List[str] = []
    for f in findings:
        lines.append(f"[{f.status}] {f.id}: {f.message}")
    return "\n".join(lines)


def emit_signals(findings: List[Finding], env: Optional[Dict[str, str]] = None) -> None:
    if signals_module is None:
        print("WARN: signals module not available; skipping signal emission.", file=sys.stderr)
        return
    records = [f.to_signal() for f in findings if f.status != "ok"]
    # include feature flags as info
    for f in findings:
        if f.id == "feature_flags":
            records.extend([
                {
                    "id": "pattern_recall_enabled",
                    "severity": "info",
                    "source": "config",
                    "constitutional_reference": "§13 Observational Memory non-authority",
                    "message": "Pattern Recall / Observational Memory layer enabled (informational only).",
                }
            ] if f.evidence.get("pattern_recall_enabled") else [])
    if not records:
        return
    signals_module.emit_signals(records, env=env)


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="CERES doctor (read-only, non-authoritative)")
    parser.add_argument("--json", dest="json_out", action="store_true", help="Output JSON to stdout")
    parser.add_argument("--emit-signals", action="store_true", help="Forward findings to Signals (append-only)")
    args = parser.parse_args(argv)

    root = DEFAULT_ROOT
    findings = run_checks(root)

    if args.json_out:
        json.dump([asdict(f) for f in findings], sys.stdout, indent=2)
        sys.stdout.write("\n")
    else:
        sys.stdout.write(render_human(findings) + "\n")

    if args.emit_signals:
        emit_signals(findings, env=os.environ)

    return 0


if __name__ == "__main__":
    sys.exit(main())
