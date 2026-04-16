#!/usr/bin/env python3
"""Detect which LLM harness is running and write capabilities to STATE.

Writes .ceres/workspace/harness.json with the detected harness identity
and its capability profile. auto-governance.py reads this to adjust
mode defaults (e.g., interactive vs autonomous enforcement).

Detection is best-effort via environment variables and known markers.
Falls back to a conservative generic profile.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict


def resolve_workspace() -> Path:
    env = os.environ.get("CERES_WORKSPACE")
    if env:
        return Path(env)
    root = Path(__file__).resolve().parent.parent
    candidate = root / ".ceres" / "workspace"
    if candidate.is_dir():
        return candidate
    return root


HARNESS_PROFILES: Dict[str, Dict[str, Any]] = {
    "claude-code": {
        "interactive_default": True,
        "permission_model": "per-command",
        "has_plan_mode": True,
        "has_background_agents": True,
        "has_web_fetch": True,
        "context_budget": "large",
    },
    "codex": {
        "interactive_default": False,
        "permission_model": "autonomous",
        "has_plan_mode": False,
        "has_background_agents": False,
        "has_web_fetch": True,
        "context_budget": "medium",
    },
    "gemini-code": {
        "interactive_default": True,
        "permission_model": "per-command",
        "has_plan_mode": False,
        "has_background_agents": False,
        "has_web_fetch": True,
        "context_budget": "large",
    },
    "cursor": {
        "interactive_default": True,
        "permission_model": "per-command",
        "has_plan_mode": False,
        "has_background_agents": False,
        "has_web_fetch": False,
        "context_budget": "medium",
    },
    "generic": {
        "interactive_default": True,
        "permission_model": "unknown",
        "has_plan_mode": False,
        "has_background_agents": False,
        "has_web_fetch": False,
        "context_budget": "small",
    },
}


def detect_harness() -> str:
    if os.environ.get("CLAUDE_CODE") or os.environ.get("CLAUDE_CODE_ENTRYPOINT"):
        return "claude-code"
    if os.environ.get("CODEX_CLI") or os.environ.get("OPENAI_API_KEY") and os.environ.get("CODEX_SANDBOX"):
        return "codex"
    if os.environ.get("GEMINI_CODE") or os.environ.get("GOOGLE_AI_STUDIO"):
        return "gemini-code"
    if os.environ.get("CURSOR_SESSION") or os.environ.get("CURSOR_TRACE_ID"):
        return "cursor"
    return "generic"


def main() -> None:
    workspace = resolve_workspace()
    harness_name = detect_harness()
    profile = HARNESS_PROFILES.get(harness_name, HARNESS_PROFILES["generic"])

    result = {
        "harness": harness_name,
        "capabilities": profile,
    }

    out_path = workspace / "harness.json"
    out_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(f"Harness detected: {harness_name} -> {out_path}")


if __name__ == "__main__":
    main()
