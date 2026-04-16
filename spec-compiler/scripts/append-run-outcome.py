#!/usr/bin/env python3
import json
import os
import sys
from pathlib import Path

REQUIRED_FIELDS = [
    "run_id",
    "timestamp",
    "concept_id",
    "skill_id",
    "spec_id",
    "files_touched",
    "commands_executed",
    "outcome",
    "fix_loop_count",
    "synchronizations_used",
]
ALIASES = {
    "commands": "commands_executed",
    "synchronizations": "synchronizations_used",
}


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def main() -> None:
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError as exc:
        fail(f"Invalid JSON input: {exc}")

    if not isinstance(payload, dict):
        fail("Input must be a JSON object.")

    for old_key, new_key in ALIASES.items():
        if old_key in payload and new_key not in payload:
            payload[new_key] = payload.pop(old_key)

    profile = os.environ.get("EXECUTION_PROFILE")
    if profile in {"SAFE", "FAST"} and "execution_profile" not in payload:
        payload["execution_profile"] = profile
    if profile == "FAST":
        scope = os.environ.get("FAST_MODE_SCOPE")
        if scope and "fast_mode_scope" not in payload:
            payload["fast_mode_scope"] = scope

    missing = [field for field in REQUIRED_FIELDS if field not in payload]
    if missing:
        fail(f"Missing required fields: {', '.join(missing)}")

    timestamp = payload.get("timestamp")
    if not isinstance(timestamp, str) or len(timestamp) < 10:
        fail("timestamp must be an ISO-like string (YYYY-MM-DD...).")

    run_id = payload.get("run_id")
    if not isinstance(run_id, str) or not run_id:
        fail("run_id must be a non-empty string.")

    run_date = timestamp[:10]
    target_dir = Path("runs") / run_date
    target_dir.mkdir(parents=True, exist_ok=True)

    target_file = target_dir / f"{run_id}.jsonl"
    with target_file.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=True))
        handle.write("\n")


if __name__ == "__main__":
    main()
