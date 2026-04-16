#!/usr/bin/env python3
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
import importlib.util
from typing import Union

ROOT = Path(__file__).resolve().parent.parent
DISCOVERY_SCRIPT = ROOT / "scripts/discover-uip-artifacts.py"

# Explicit allowlist for suppressing schema checks (repo-relative paths only).
ALLOWLIST_PATHS = {
    # "path/to/artifact.intent.json",
}

UI_EVENT_TYPES = {
    "form.submitted",
    "action.clicked",
    "modal.confirmed",
    "modal.cancelled",
    "table.rowSelected",
}
UI_EVENT_SCHEMA_VERSIONS = {"1.0.0"}


def fail(category: str, file_path: Union[Path, str], rule: str, suggestion: str) -> None:
    if isinstance(file_path, Path):
        try:
            display_path: Union[Path, str] = file_path.relative_to(ROOT)
        except ValueError:
            display_path = file_path
    else:
        display_path = file_path
    message = (
        f"{category} | file: {display_path} | rule: {rule} | suggestion: {suggestion}"
    )
    print(message, file=sys.stderr)
    raise SystemExit(1)


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


def load_intent_validator():
    module_path = ROOT / "skills/ui-intent-emit/impl/run.py"
    spec = importlib.util.spec_from_file_location("ui_intent_run", module_path)
    if spec is None or spec.loader is None:
        fail(
            "UIP-STRUCTURAL-VIOLATION",
            module_path,
            "intent.validator",
            "Ensure the UI intent validator is present and importable.",
        )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    if not hasattr(module, "validate_intent"):
        fail(
            "UIP-STRUCTURAL-VIOLATION",
            module_path,
            "intent.validator",
            "Expose validate_intent in the UI intent validator module.",
        )
    if not hasattr(module, "ALLOWED_TYPES") or not hasattr(module, "SCHEMA_VERSION"):
        fail(
            "UIP-STRUCTURAL-VIOLATION",
            module_path,
            "intent.validator",
            "Expose ALLOWED_TYPES and SCHEMA_VERSION in the UI intent validator.",
        )
    return module


def run_discovery() -> list[dict[str, str]]:
    result = subprocess.run(
        [sys.executable, str(DISCOVERY_SCRIPT)],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        message = (result.stderr or result.stdout).strip()
        if message:
            print(message, file=sys.stderr)
        raise SystemExit(result.returncode)

    artifacts: list[dict[str, str]] = []
    for line in result.stdout.splitlines():
        if not line.strip():
            continue
        try:
            artifact = json.loads(line)
        except json.JSONDecodeError:
            fail(
                "UIP-STRUCTURAL-VIOLATION",
                DISCOVERY_SCRIPT,
                "discovery.output",
                "Ensure discovery emits JSON lines with path/type.",
            )
        if "path" not in artifact or "type" not in artifact:
            fail(
                "UIP-STRUCTURAL-VIOLATION",
                DISCOVERY_SCRIPT,
                "discovery.output",
                "Ensure discovery emits path/type for every artifact.",
            )
        artifacts.append(artifact)
    return artifacts


def validate_intent(path: Path, data: dict, intent_module) -> None:
    schema_version = getattr(intent_module, "SCHEMA_VERSION")
    allowed_types = set(getattr(intent_module, "ALLOWED_TYPES"))

    if not is_non_empty_string(data.get("schemaVersion")):
        fail(
            "UIP-SCHEMA-VIOLATION",
            path,
            "intent.schemaVersion",
            "Set schemaVersion to the current UIP intent schema version.",
        )
    if data.get("schemaVersion") != schema_version:
        fail(
            "UIP-SCHEMA-VIOLATION",
            path,
            "intent.schemaVersion",
            "Update schemaVersion to the supported UIP intent schema version.",
        )
    if not is_non_empty_string(data.get("id")):
        fail(
            "UIP-SCHEMA-VIOLATION",
            path,
            "intent.id",
            "Set id to a non-empty string.",
        )
    intent_type = data.get("type")
    if not is_non_empty_string(intent_type) or intent_type not in allowed_types:
        fail(
            "UIP-SCHEMA-VIOLATION",
            path,
            "intent.type",
            "Set type to a supported UI intent enum value.",
        )
    purpose = data.get("purpose")
    if not is_object(purpose) or not is_non_empty_string(purpose.get("summary")):
        fail(
            "UIP-SCHEMA-VIOLATION",
            path,
            "intent.purpose.summary",
            "Set purpose.summary to a non-empty string.",
        )
    if "payload" not in data or not is_object(data.get("payload")):
        fail(
            "UIP-SCHEMA-VIOLATION",
            path,
            "intent.payload",
            "Add a payload object (it may be empty).",
        )

    validate_intent_fn = getattr(intent_module, "validate_intent")
    errors = validate_intent_fn(data)
    if errors:
        first = errors[0]
        path_label = first.get("path")
        suggestion = first.get("message") or "Resolve the intent schema violation."
        rule = "intent.root" if not path_label else f"intent.{path_label}"
        fail("UIP-SCHEMA-VIOLATION", path, rule, suggestion)


def validate_event(path: Path, data: dict) -> None:
    if not is_non_empty_string(data.get("schemaVersion")):
        fail(
            "UIP-SCHEMA-VIOLATION",
            path,
            "event.schemaVersion",
            "Set schemaVersion to the current UIP event schema version.",
        )
    if data.get("schemaVersion") not in UI_EVENT_SCHEMA_VERSIONS:
        fail(
            "UIP-SCHEMA-VIOLATION",
            path,
            "event.schemaVersion",
            "Update schemaVersion to a supported UIP event schema version.",
        )
    if not is_non_empty_string(data.get("id")):
        fail(
            "UIP-SCHEMA-VIOLATION",
            path,
            "event.id",
            "Set id to a non-empty string.",
        )
    if not is_iso8601(data.get("ts")):
        fail(
            "UIP-SCHEMA-VIOLATION",
            path,
            "event.ts",
            "Set ts to an ISO-8601 timestamp.",
        )
    if not is_non_empty_string(data.get("intentId")):
        fail(
            "UIP-SCHEMA-VIOLATION",
            path,
            "event.intentId",
            "Set intentId to a non-empty string.",
        )
    event_type = data.get("type")
    if not is_non_empty_string(event_type) or event_type not in UI_EVENT_TYPES:
        fail(
            "UIP-SCHEMA-VIOLATION",
            path,
            "event.type",
            "Set type to a supported UI event enum value.",
        )
    if not is_non_empty_string(data.get("idempotencyKey")):
        fail(
            "UIP-SCHEMA-VIOLATION",
            path,
            "event.idempotencyKey",
            "Set idempotencyKey to a non-empty string.",
        )
    if not is_non_empty_string(data.get("uiSessionId")):
        fail(
            "UIP-SCHEMA-VIOLATION",
            path,
            "event.uiSessionId",
            "Set uiSessionId to a non-empty string.",
        )
    if "payload" not in data or not is_object(data.get("payload")):
        fail(
            "UIP-SCHEMA-VIOLATION",
            path,
            "event.payload",
            "Add a payload object (it may be empty).",
        )


def main() -> None:
    intent_module = load_intent_validator()
    artifacts = run_discovery()
    for artifact in artifacts:
        artifact_path = Path(artifact["path"])
        try:
            relative = artifact_path.relative_to(ROOT).as_posix()
        except ValueError:
            relative = artifact_path.as_posix()
        if relative in ALLOWLIST_PATHS:
            continue

        try:
            payload = json.loads(artifact_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            fail(
                "UIP-STRUCTURAL-VIOLATION",
                artifact_path,
                "valid-json",
                "Fix JSON syntax so the artifact can be parsed.",
            )

        if not isinstance(payload, dict):
            fail(
                "UIP-SCHEMA-VIOLATION",
                artifact_path,
                "artifact.root",
                "Ensure the artifact is a JSON object.",
            )

        artifact_type = artifact.get("type")
        if artifact_type == "intent":
            validate_intent(artifact_path, payload, intent_module)
        elif artifact_type == "event":
            validate_event(artifact_path, payload)
        else:
            fail(
                "UIP-STRUCTURAL-VIOLATION",
                artifact_path,
                "artifact.type",
                "Ensure artifacts are tagged as intent or event during discovery.",
            )


if __name__ == "__main__":
    main()
