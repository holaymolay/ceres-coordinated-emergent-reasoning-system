#!/usr/bin/env python3
import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Union

from uip_yaml import YamlError, load_yaml

ROOT = Path(__file__).resolve().parent.parent
DISCOVERY_SCRIPT = ROOT / "scripts/discover-uip-artifacts.py"

UI_EVENT_TYPES = {
    "form.submitted",
    "action.clicked",
    "modal.confirmed",
    "modal.cancelled",
    "table.rowSelected",
}


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


def run_event_discovery() -> dict[str, Path]:
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

    event_types: dict[str, Path] = {}
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
        if artifact.get("type") != "event":
            continue
        path = Path(artifact["path"])
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            fail(
                "UIP-STRUCTURAL-VIOLATION",
                path,
                "valid-json",
                "Fix JSON syntax so the event artifact can be parsed.",
            )
        event_type = payload.get("type")
        if not isinstance(event_type, str) or not event_type.strip():
            fail(
                "UIP-SCHEMA-VIOLATION",
                path,
                "event.type",
                "Set type to a non-empty UIEvent type string.",
            )
        event_types.setdefault(event_type, path)
    return event_types


def discover_sync_manifests() -> list[Path]:
    paths: set[Path] = set()
    paths.update(ROOT.rglob("*.sync.yaml"))
    for folder in [
        ROOT / "synchronizations",
        ROOT / "synchronizations" / "templates",
        ROOT / "synchronizations" / "examples",
    ]:
        if not folder.exists():
            continue
        paths.update(folder.glob("*.yaml"))
        paths.update(folder.glob("*.yml"))
    return sorted(paths)


def ensure_mapping(
    path: Path,
    data: dict[str, Any],
    field: str,
    rule: str,
    suggestion: str,
) -> dict[str, Any]:
    value = data.get(field)
    if not isinstance(value, dict):
        fail("UIP-SCHEMA-VIOLATION", path, rule, suggestion)
    return value


def validate_sync_manifest(path: Path, data: Any) -> set[str]:
    if not isinstance(data, dict):
        fail(
            "UIP-SCHEMA-VIOLATION",
            path,
            "sync.manifest",
            "Ensure the synchronization manifest is a YAML mapping.",
        )

    trigger = ensure_mapping(
        path,
        data,
        "trigger",
        "sync.trigger",
        "Add trigger.source, trigger.field, and trigger.match.",
    )
    source = trigger.get("source")
    field = trigger.get("field")
    if source != "ui_event" or field != "type":
        fail(
            "UIP-SCHEMA-VIOLATION",
            path,
            "sync.trigger",
            "Set trigger.source to ui_event and trigger.field to type.",
        )
    match = trigger.get("match")
    if isinstance(match, str):
        match_values = [match]
    elif isinstance(match, list):
        match_values = match
    else:
        match_values = []
    if not match_values:
        fail(
            "UIP-SCHEMA-VIOLATION",
            path,
            "sync.trigger.match",
            "List at least one UIEvent type under trigger.match.",
        )
    event_types: set[str] = set()
    for value in match_values:
        if not isinstance(value, str) or not value.strip():
            fail(
                "UIP-SCHEMA-VIOLATION",
                path,
                "sync.trigger.match",
                "Ensure trigger.match entries are non-empty strings.",
            )
        if value not in UI_EVENT_TYPES:
            fail(
                "UIP-SCHEMA-VIOLATION",
                path,
                f"UIP violation: synchronization references unknown UIEvent type '{value}'",
                "Use a known UIEvent type or update the UIEvent schema list.",
            )
        event_types.add(value)

    participants = data.get("participants")
    if not isinstance(participants, list) or not participants:
        fail(
            "UIP-SCHEMA-VIOLATION",
            path,
            "sync.participants",
            "Provide at least one participant with a concept name.",
        )
    for participant in participants:
        if not isinstance(participant, dict):
            fail(
                "UIP-SCHEMA-VIOLATION",
                path,
                "sync.participants",
                "Participant entries must be mappings with concept/handler.",
            )
        concept = participant.get("concept")
        handler = participant.get("handler")
        if not isinstance(concept, str) or not concept.strip():
            fail(
                "UIP-SCHEMA-VIOLATION",
                path,
                "sync.participants.concept",
                "Set participants.concept to a non-empty Concept name.",
            )
        if not isinstance(handler, str) or not handler.strip():
            fail(
                "UIP-SCHEMA-VIOLATION",
                path,
                "sync.participants.handler",
                "Set participants.handler to a non-empty handler id.",
            )

    mapping = ensure_mapping(
        path,
        data,
        "mapping",
        "sync.mapping",
        "Define mapping.target.fields for payload routing.",
    )
    target = ensure_mapping(
        path,
        mapping,
        "target",
        "sync.mapping.target",
        "Define mapping.target.fields for payload routing.",
    )
    fields = ensure_mapping(
        path,
        target,
        "fields",
        "sync.mapping.target.fields",
        "Define mapping.target.fields including payload.",
    )
    if "payload" not in fields:
        fail(
            "UIP-SCHEMA-VIOLATION",
            path,
            "sync.mapping.payload",
            "Add payload mapping under mapping.target.fields.",
        )

    constraints = ensure_mapping(
        path,
        data,
        "constraints",
        "sync.constraints",
        "Define constraints.idempotent and constraints.authScope.",
    )
    if "idempotent" not in constraints:
        fail(
            "UIP-SCHEMA-VIOLATION",
            path,
            "sync.constraints.idempotent",
            "Declare constraints.idempotent to document idempotency behavior.",
        )
    auth_scope = constraints.get("authScope")
    if not isinstance(auth_scope, str) or not auth_scope.strip():
        fail(
            "UIP-SCHEMA-VIOLATION",
            path,
            "sync.constraints.authScope",
            "Set constraints.authScope to a non-empty scope string.",
        )

    return event_types


def main() -> None:
    event_types = run_event_discovery()
    sync_paths = discover_sync_manifests()
    if not sync_paths:
        if event_types:
            first_event = next(iter(event_types.values()))
            fail(
                "UIP-BOUNDARY-VIOLATION",
                first_event,
                "UIP violation: UIEvent type has no synchronization",
                "Add a Synchronization manifest that routes this UIEvent.",
            )
        return

    sync_event_types: set[str] = set()
    for path in sync_paths:
        try:
            manifest = load_yaml(path)
        except YamlError as exc:
            fail(
                "UIP-SCHEMA-VIOLATION",
                path,
                "sync.yaml",
                f"Fix YAML syntax: {exc}",
            )
        sync_event_types.update(validate_sync_manifest(path, manifest))

    for event_type, path in event_types.items():
        if event_type not in sync_event_types:
            fail(
                "UIP-BOUNDARY-VIOLATION",
                path,
                f"UIP violation: UIEvent type '{event_type}' has no synchronization",
                "Add a Synchronization trigger for this UIEvent type.",
            )


if __name__ == "__main__":
    main()
