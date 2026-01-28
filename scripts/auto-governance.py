#!/usr/bin/env python3
"""Auto-toggle governance based on workspace health signals."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parent.parent
STATE_PATH = ROOT / "modes_settings_profiles.json"


def load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Dict[str, Any]) -> None:
    path.write_text(json.dumps(data, indent=2, sort_keys=False) + "\n", encoding="utf-8")


def workspace_root() -> Path:
    env = os.environ.get("CERES_WORKSPACE")
    if env:
        return Path(env)
    candidate = ROOT / ".ceres" / "workspace"
    if candidate.exists():
        return candidate
    return ROOT


def parse_front_matter(text: str) -> Dict[str, Any]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    data: Dict[str, Any] = {}
    current_key = None
    for line in lines[1:]:
        if line.strip() == "---":
            break
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if ":" in stripped and not stripped.startswith("-"):
            key, value = stripped.split(":", 1)
            key = key.strip()
            value = value.strip()
            current_key = None
            if value == "":
                data[key] = []
                current_key = key
            elif value.lower() in {"true", "false"}:
                data[key] = value.lower() == "true"
            else:
                data[key] = value.strip("\"'")
        elif stripped.startswith("-") and current_key:
            item = stripped.lstrip("-").strip()
            if item:
                data.setdefault(current_key, [])
                if isinstance(data[current_key], list):
                    data[current_key].append(item)
    return data


def detect_issues(workspace: Path) -> List[str]:
    issues: List[str] = []

    objective = workspace / "objective-contract.json"
    if not objective.exists():
        issues.append("objective_contract_missing")
    else:
        try:
            data = load_json(objective)
            if data.get("status") != "committed":
                issues.append("objective_contract_not_committed")
        except Exception:
            issues.append("objective_contract_parse_error")

    gap = workspace / "gap-ledger.json"
    if not gap.exists():
        issues.append("gap_ledger_missing")
    else:
        try:
            data = load_json(gap)
            gaps = data.get("gaps", [])
            for entry in gaps:
                if isinstance(entry, dict) and entry.get("blocking") is True and entry.get("status") != "resolved":
                    issues.append("blocking_gap_unresolved")
                    break
        except Exception:
            issues.append("gap_ledger_parse_error")

    elicitation_dir = workspace / "specs" / "elicitation"
    if not elicitation_dir.exists():
        issues.append("elicitation_missing")
    else:
        files = sorted(p for p in elicitation_dir.glob("*.md") if p.is_file())
        if not files:
            issues.append("elicitation_missing")
        else:
            data = parse_front_matter(files[0].read_text(encoding="utf-8"))
            if data.get("ready_for_planning") is not True:
                issues.append("elicitation_not_ready")
            blocking = data.get("blocking_unknowns")
            if isinstance(blocking, list) and blocking:
                issues.append("elicitation_blocking_unknowns")

    report_candidates = [
        workspace / "logs" / "prompt-debug-report.yaml",
        ROOT / "logs" / "prompt-debug-report.yaml",
    ]
    for report in report_candidates:
        if report.exists():
            try:
                import yaml  # type: ignore
            except Exception:
                break
            try:
                data = yaml.safe_load(report.read_text(encoding="utf-8")) or {}
                if data.get("status") and data.get("status") != "approved":
                    issues.append("prompt_debugger_not_approved")
            except Exception:
                issues.append("prompt_debugger_parse_error")
            break

    return sorted(set(issues))


def apply_overrides(state: Dict[str, Any], strict: bool) -> Dict[str, Any]:
    overrides = state.get("session_overrides") if isinstance(state.get("session_overrides"), dict) else {}
    strict_values = {
        "execution_allowed": False,
        "enforcement": "strict",
        "execution_continuity": "manual",
        "prompt_debugger": "blocking",
        "intake_required": "manual",
        "spec_elicitation": "manual",
        "gap_ledger": "manual",
    }
    fast_values = {
        "execution_allowed": True,
        "enforcement": "warn",
        "execution_continuity": "auto-safe",
        "prompt_debugger": "non-blocking",
        "intake_required": "auto-generate",
        "spec_elicitation": "auto-generate-skeleton",
        "gap_ledger": "auto-append",
    }
    values = strict_values if strict else fast_values
    overrides.update(values)
    state["session_overrides"] = overrides
    return state


def emit_event(status: str, issues: List[str]) -> None:
    helper = ROOT / "scripts" / "log_event.py"
    if not helper.exists():
        return
    payload = json.dumps({"issues": issues})
    os.system(f"{helper} --type auto_governance --status {status} --message \"auto governance\" --context '{payload}'")


def main() -> int:
    if not STATE_PATH.exists():
        return 0
    workspace = workspace_root()
    issues = detect_issues(workspace)
    strict = bool(issues)
    state = load_json(STATE_PATH)
    state = apply_overrides(state, strict)
    write_json(STATE_PATH, state)
    emit_event("warn" if strict else "info", issues)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
