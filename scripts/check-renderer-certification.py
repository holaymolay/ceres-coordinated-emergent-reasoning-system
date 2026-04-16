#!/usr/bin/env python3
import json
import sys
from pathlib import Path
from typing import Any, Union
import importlib.util

from uip_yaml import YamlError, load_yaml

ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = ROOT / "ui-contracts/renderers.yaml"

REQUIRED_EVENT_FIELDS = {"intentId", "uiSessionId", "idempotencyKey", "schemaVersion"}
NONDETERMINISTIC_TOKENS = ("Math.random", "Date.now", "new Date(", "crypto.randomUUID")


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


def load_intent_validator():
    module_path = ROOT / "skills/ui-intent-emit/impl/run.py"
    spec = importlib.util.spec_from_file_location("ui_intent_run", module_path)
    if spec is None or spec.loader is None:
        fail(
            "UIP-STRUCTURAL-VIOLATION",
            module_path,
            "renderer.intent.validator",
            "Ensure the UI intent validator is present and importable.",
        )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    if not hasattr(module, "validate_intent"):
        fail(
            "UIP-STRUCTURAL-VIOLATION",
            module_path,
            "renderer.intent.validator",
            "Expose validate_intent in the UI intent validator module.",
        )
    return module


def load_manifest() -> list[dict[str, Any]]:
    try:
        data = load_yaml(MANIFEST_PATH)
    except YamlError as exc:
        fail(
            "UIP-STRUCTURAL-VIOLATION",
            MANIFEST_PATH,
            "renderer.manifest",
            f"Fix renderer manifest YAML: {exc}",
        )
    if not isinstance(data, dict) or "renderers" not in data:
        fail(
            "UIP-STRUCTURAL-VIOLATION",
            MANIFEST_PATH,
            "renderer.manifest",
            "Add a renderers list to the renderer manifest.",
        )
    renderers = data.get("renderers")
    if not isinstance(renderers, list) or not renderers:
        fail(
            "UIP-STRUCTURAL-VIOLATION",
            MANIFEST_PATH,
            "renderer.manifest",
            "Provide at least one renderer entry.",
        )
    return renderers


def read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        fail(
            "UIP-STRUCTURAL-VIOLATION",
            path,
            "valid-json",
            "Fix JSON syntax so the fixture can be parsed.",
        )


def validate_event_fixture(path: Path, payload: Any) -> None:
    if not isinstance(payload, dict):
        fail(
            "UIP-SCHEMA-VIOLATION",
            path,
            "renderer.output.event",
            "Ensure the event fixture is a JSON object.",
        )
    missing = REQUIRED_EVENT_FIELDS - payload.keys()
    if missing:
        fail(
            "UIP-SCHEMA-VIOLATION",
            path,
            "renderer.output.event",
            f"Add missing UIEvent fields: {', '.join(sorted(missing))}.",
        )
    for field in REQUIRED_EVENT_FIELDS:
        value = payload.get(field)
        if not isinstance(value, str) or not value.strip():
            fail(
                "UIP-SCHEMA-VIOLATION",
                path,
                "renderer.output.event",
                f"Set {field} to a non-empty string.",
            )
    if "payload" not in payload or not isinstance(payload.get("payload"), dict):
        fail(
            "UIP-SCHEMA-VIOLATION",
            path,
            "renderer.output.event",
            "Ensure payload is a JSON object.",
        )


def ensure_no_disallowed_imports(path: Path, text: str) -> None:
    for token in ("concepts/", "agents/", "skills/"):
        if token in text:
            fail(
                "UIP-BOUNDARY-VIOLATION",
                path,
                "renderer.imports",
                "Remove domain/agent/skill imports from renderer code.",
            )


def ensure_determinism(path: Path, text: str) -> None:
    for token in NONDETERMINISTIC_TOKENS:
        if token in text:
            fail(
                "UIP-BOUNDARY-VIOLATION",
                path,
                "renderer.determinism",
                f"Remove nondeterministic call ({token}).",
            )


def ensure_tokenized_styling(path: Path, text: str) -> None:
    if "tailwindTokens" not in text:
        fail(
            "UIP-BOUNDARY-VIOLATION",
            path,
            "renderer.styling",
            "Use adapter token imports for styling.",
        )
    if 'className="' in text or "className='" in text:
        fail(
            "UIP-BOUNDARY-VIOLATION",
            path,
            "renderer.styling",
            "Avoid inline className strings; use token references.",
        )


def ensure_validation_call(path: Path, text: str) -> None:
    if "assertValidUiIntent" not in text and "validateUiIntent" not in text:
        fail(
            "UIP-BOUNDARY-VIOLATION",
            path,
            "renderer.input.validation",
            "Call assertValidUiIntent or validateUiIntent before rendering.",
        )


def main() -> None:
    intent_module = load_intent_validator()
    validate_intent_fn = getattr(intent_module, "validate_intent")
    renderers = load_manifest()

    for renderer in renderers:
        if not isinstance(renderer, dict):
            fail(
                "UIP-STRUCTURAL-VIOLATION",
                MANIFEST_PATH,
                "renderer.manifest",
                "Renderer entries must be mappings.",
            )
        entrypoint = renderer.get("entrypoint")
        adapter = renderer.get("adapter")
        intent_fixture = renderer.get("intentFixture")
        invalid_intent_fixture = renderer.get("invalidIntentFixture")
        event_fixture = renderer.get("eventFixture")

        for key, value in [
            ("entrypoint", entrypoint),
            ("adapter", adapter),
            ("intentFixture", intent_fixture),
            ("invalidIntentFixture", invalid_intent_fixture),
            ("eventFixture", event_fixture),
        ]:
            if not isinstance(value, str) or not value.strip():
                fail(
                    "UIP-STRUCTURAL-VIOLATION",
                    MANIFEST_PATH,
                    "renderer.manifest",
                    f"Set {key} to a non-empty path string.",
                )

        entry_path = ROOT / entrypoint
        adapter_path = ROOT / adapter
        if not entry_path.exists():
            fail(
                "UIP-STRUCTURAL-VIOLATION",
                entry_path,
                "renderer.entrypoint",
                "Ensure the renderer entrypoint file exists.",
            )
        if not adapter_path.exists():
            fail(
                "UIP-STRUCTURAL-VIOLATION",
                adapter_path,
                "renderer.adapter",
                "Ensure the renderer adapter file exists.",
            )

        entry_text = entry_path.read_text(encoding="utf-8")
        adapter_text = adapter_path.read_text(encoding="utf-8")

        ensure_validation_call(entry_path, entry_text)
        ensure_no_disallowed_imports(entry_path, entry_text)
        ensure_no_disallowed_imports(adapter_path, adapter_text)
        ensure_determinism(entry_path, entry_text)
        ensure_determinism(adapter_path, adapter_text)
        ensure_tokenized_styling(adapter_path, adapter_text)

        valid_intent = read_json(ROOT / intent_fixture)
        intent_errors = validate_intent_fn(valid_intent)
        if intent_errors:
            fail(
                "UIP-SCHEMA-VIOLATION",
                ROOT / intent_fixture,
                "renderer.input.valid",
                "Fix the valid UIIntent fixture to pass validation.",
            )

        invalid_payload = read_json(ROOT / invalid_intent_fixture)
        invalid_intent = invalid_payload.get("intent") if isinstance(invalid_payload, dict) else None
        if invalid_intent is None:
            invalid_intent = invalid_payload
        invalid_errors = validate_intent_fn(invalid_intent)
        if not invalid_errors:
            fail(
                "UIP-SCHEMA-VIOLATION",
                ROOT / invalid_intent_fixture,
                "renderer.input.invalid",
                "Provide an invalid UIIntent fixture that fails validation.",
            )
        if not any(error.get("path") == "schemaVersion" for error in invalid_errors):
            fail(
                "UIP-SCHEMA-VIOLATION",
                ROOT / invalid_intent_fixture,
                "renderer.input.schemaVersion",
                "Ensure the invalid fixture triggers schemaVersion rejection.",
            )

        event_payload = read_json(ROOT / event_fixture)
        validate_event_fixture(ROOT / event_fixture, event_payload)


if __name__ == "__main__":
    main()
