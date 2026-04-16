#!/usr/bin/env python3
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
DISCOVERY_SCRIPT = ROOT / "scripts/discover-uip-artifacts.py"

INTENT_SCHEMA_VERSION = "0.2.0"
EVENT_SCHEMA_VERSION = "0.2.0"

INTENT_TYPES = {
    "page.create",
    "form.create",
    "table.create",
    "modal.open",
    "alert.show",
    "cta.request",
}
EVENT_TYPES = {
    "form.submitted",
    "action.clicked",
    "modal.confirmed",
    "modal.cancelled",
    "table.rowSelected",
}


def is_non_empty_string(value: object) -> bool:
    return isinstance(value, str) and len(value.strip()) > 0


def is_object(value: object) -> bool:
    return isinstance(value, dict)


def is_iso8601(value: object) -> bool:
    if not isinstance(value, str) or not value:
        return False
    try:
        if value.endswith("Z"):
            datetime.fromisoformat(value.replace("Z", "+00:00"))
        else:
            datetime.fromisoformat(value)
        return True
    except ValueError:
        return False


def run_discovery() -> list[dict[str, str]]:
    result = subprocess.run(
        [sys.executable, str(DISCOVERY_SCRIPT)],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        message = (result.stderr or result.stdout).strip()
        print("UIP-0.2 Shadow Validation Results")
        if message:
            print(f"Shadow validation skipped: {message}")
        else:
            print("Shadow validation skipped: discovery failed.")
        return []

    artifacts: list[dict[str, str]] = []
    for line in result.stdout.splitlines():
        if not line.strip():
            continue
        try:
            artifacts.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return artifacts


def validate_intent(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if data.get("schemaVersion") != INTENT_SCHEMA_VERSION:
        errors.append("schemaVersion must be 0.2.0")
    if not is_non_empty_string(data.get("id")):
        errors.append("id must be a non-empty string")
    intent_type = data.get("type")
    if not is_non_empty_string(intent_type) or intent_type not in INTENT_TYPES:
        errors.append("type must be a supported intent type")
    purpose = data.get("purpose")
    if not is_object(purpose) or not is_non_empty_string(purpose.get("summary")):
        errors.append("purpose.summary must be a non-empty string")
    if "payload" not in data or not is_object(data.get("payload")):
        errors.append("payload must be an object")
    components = data.get("components")
    if not is_object(components):
        errors.append("components must be an object")
    return errors


def validate_event(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if data.get("schemaVersion") != EVENT_SCHEMA_VERSION:
        errors.append("schemaVersion must be 0.2.0")
    if not is_non_empty_string(data.get("id")):
        errors.append("id must be a non-empty string")
    if not is_iso8601(data.get("ts")):
        errors.append("ts must be ISO-8601")
    if not is_non_empty_string(data.get("intentId")):
        errors.append("intentId must be a non-empty string")
    event_type = data.get("type")
    if not is_non_empty_string(event_type) or event_type not in EVENT_TYPES:
        errors.append("type must be a supported event type")
    if not is_non_empty_string(data.get("uiSessionId")):
        errors.append("uiSessionId must be a non-empty string")
    if not is_non_empty_string(data.get("idempotencyKey")):
        errors.append("idempotencyKey must be a non-empty string")
    if "payload" not in data or not is_object(data.get("payload")):
        errors.append("payload must be an object")
    return errors


def main() -> None:
    artifacts = run_discovery()
    failures: list[tuple[Path, list[str]]] = []

    for artifact in artifacts:
        path = Path(artifact.get("path", ""))
        if not path.exists():
            continue
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            failures.append((path, ["invalid JSON"]))
            continue
        if not isinstance(payload, dict):
            failures.append((path, ["artifact must be a JSON object"]))
            continue
        if artifact.get("type") == "intent":
            errors = validate_intent(payload)
        elif artifact.get("type") == "event":
            errors = validate_event(payload)
        else:
            errors = ["unknown artifact type"]
        if errors:
            failures.append((path, errors))

    print("UIP-0.2 Shadow Validation Results")
    if not artifacts:
        print("No artifacts discovered.")
        return
    if not failures:
        print("All artifacts pass UIP-0.2 shadow validation.")
        return

    print(f"{len(failures)} artifact(s) would fail under UIP-0.2.")
    for path, errors in failures:
        try:
            display = path.relative_to(ROOT)
        except ValueError:
            display = path
        reason = "; ".join(errors)
        print(f"- {display}: {reason}")


if __name__ == "__main__":
    main()
