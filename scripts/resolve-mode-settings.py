#!/usr/bin/env python3
"""
Resolve modes/settings/profiles with guarded enforcement.

Responsibilities:
- Enforce precedence: system_defaults -> mode_defaults -> profile_overrides -> session_overrides.
- Block illegal combinations (professional + execution_continuity=continuous).
- Apply auto-safe predicate (requires flags).
- Emit active mode/profile and effective settings to events.jsonl.

No UX changes. No governance changes. Single-purpose resolver.
"""

import argparse
import json
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STATE_PATH = ROOT / "modes_settings_profiles.json"
EVENTS_PATH = ROOT / "events.jsonl"

SCHEMA_SETTINGS_KEYS = [
    "execution_continuity",
    "autonomy_level",
    "questioning_policy",
    "output_density",
    "failure_handling",
    "progress_signaling",
    "safety_level",
]


def load_state() -> dict:
    if not STATE_PATH.exists():
        raise SystemExit(f"Missing configuration: {STATE_PATH}")
    try:
        return json.loads(STATE_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        raise SystemExit(f"Invalid JSON in {STATE_PATH}")


def select_mode_defaults(state: dict, active_mode: str) -> dict:
    for entry in state.get("mode_defaults", []):
        if entry.get("mode") == active_mode:
            return entry.get("settings", {})
    return {}


def select_profile_overrides(state: dict, active_profile: str | None) -> tuple[str | None, dict]:
    if not active_profile:
        return None, {}
    for entry in state.get("profiles", []):
        if entry.get("name") == active_profile:
            base_mode = entry.get("base_mode")
            return base_mode, entry.get("overrides", {})
    raise SystemExit(f"Active profile '{active_profile}' not found in configuration.")


def enforce_illegal_combinations(active_mode: str, effective: dict) -> None:
    if active_mode == "professional" and effective.get("execution_continuity") == "continuous":
        raise SystemExit("Mode enforcement failed: professional mode cannot run with execution_continuity=continuous.")


def enforce_auto_safe_predicate(args: argparse.Namespace, effective: dict) -> None:
    if effective.get("execution_continuity") != "auto-safe":
        return
    if effective.get("safety_level") == "maximal":
        raise SystemExit("Auto-safe blocked: safety_level=maximal.")
    missing = []
    if not args.blocking_gaps_resolved:
        missing.append("blocking gaps unresolved")
    if not args.no_open_clarifications:
        missing.append("open ClarificationRequest")
    if not args.deterministic_acceptance:
        missing.append("acceptance criteria not deterministic")
    if missing:
        raise SystemExit("Auto-safe blocked: " + "; ".join(missing))


def resolve_effective(state: dict) -> tuple[str, str | None, dict]:
    active_mode = state.get("active_mode", "guided")
    active_profile = state.get("active_profile")
    system_defaults = state.get("system_defaults", {})
    mode_defaults = select_mode_defaults(state, active_mode)

    base_mode_from_profile, profile_overrides = select_profile_overrides(state, active_profile)
    if base_mode_from_profile:
        active_mode = base_mode_from_profile
        mode_defaults = select_mode_defaults(state, active_mode)

    session_overrides = state.get("session_overrides", {})

    effective = {}
    for key in SCHEMA_SETTINGS_KEYS:
        if key in system_defaults:
            effective[key] = system_defaults[key]
        if key in mode_defaults:
            effective[key] = mode_defaults[key]
        if key in profile_overrides:
            effective[key] = profile_overrides[key]
        if key in session_overrides:
            effective[key] = session_overrides[key]
    return active_mode, active_profile, effective


def emit_event(active_mode: str, active_profile: str | None, effective: dict) -> None:
    event = {
        "event": "mode_profile_resolved",
        "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "source": "resolve-mode-settings.py",
        "active_mode": active_mode,
        "active_profile": active_profile,
        "effective_settings": effective,
        "run_id": str(uuid.uuid4()),
    }
    with EVENTS_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event, separators=(",", ":")) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Resolve modes/settings/profiles with enforcement.")
    parser.add_argument("--blocking-gaps-resolved", action="store_true", help="All blocking gaps resolved (required for auto-safe).")
    parser.add_argument("--no-open-clarifications", action="store_true", help="No open ClarificationRequest (required for auto-safe).")
    parser.add_argument("--deterministic-acceptance", action="store_true", help="Acceptance criteria are deterministic (required for auto-safe).")
    args = parser.parse_args()

    state = load_state()
    active_mode, active_profile, effective = resolve_effective(state)
    enforce_illegal_combinations(active_mode, effective)
    enforce_auto_safe_predicate(args, effective)
    emit_event(active_mode, active_profile, effective)
    sys.stdout.write(json.dumps({
        "active_mode": active_mode,
        "active_profile": active_profile,
        "effective_settings": effective,
    }, indent=2))


+if __name__ == "__main__":
+    main()
