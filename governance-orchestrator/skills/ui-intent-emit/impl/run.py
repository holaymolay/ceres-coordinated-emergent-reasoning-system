#!/usr/bin/env python3
import json
import sys
from typing import Any, Dict, List

SCHEMA_VERSION = "1.0.0"
ALLOWED_TYPES = {
    "page.create",
    "form.create",
    "table.create",
    "modal.open",
    "alert.show",
    "cta.request",
}
ALLOWED_SEVERITIES = {"info", "warning", "error", "success"}
BANNED_KEYS = {"jsx", "html", "tailwind", "class", "className", "style"}


def error(path: str, message: str) -> Dict[str, str]:
    return {"path": path, "message": message}


def is_non_empty_string(value: Any) -> bool:
    return isinstance(value, str) and len(value.strip()) > 0


def is_dict(value: Any) -> bool:
    return isinstance(value, dict)


def find_banned_keys(node: Any, path: str, errors: List[Dict[str, str]]) -> None:
    if isinstance(node, dict):
        for key, value in node.items():
            current_path = f"{path}.{key}" if path else key
            if key in BANNED_KEYS:
                errors.append(error(current_path, f"Banned key detected: {key}"))
            find_banned_keys(value, current_path, errors)
    elif isinstance(node, list):
        for index, value in enumerate(node):
            current_path = f"{path}[{index}]"
            find_banned_keys(value, current_path, errors)


def validate_intent(intent: Any) -> List[Dict[str, str]]:
    errors: List[Dict[str, str]] = []

    if not is_dict(intent):
        return [error("", "intent must be an object")]

    find_banned_keys(intent, "", errors)

    if intent.get("schemaVersion") != SCHEMA_VERSION:
        errors.append(error("schemaVersion", "Unsupported or missing schemaVersion"))

    if not is_non_empty_string(intent.get("id")):
        errors.append(error("id", "id must be a non-empty string"))

    intent_type = intent.get("type")
    if not is_non_empty_string(intent_type) or intent_type not in ALLOWED_TYPES:
        errors.append(error("type", "type must be a supported intent type"))

    purpose = intent.get("purpose")
    if not is_dict(purpose) or not is_non_empty_string(purpose.get("summary")):
        errors.append(error("purpose.summary", "purpose.summary must be a non-empty string"))

    components = intent.get("components")
    if not is_dict(components):
        errors.append(error("components", "components must be an object"))
    else:
        if not isinstance(components.get("fields"), list):
            errors.append(error("components.fields", "fields must be an array"))
        if not isinstance(components.get("columns"), list):
            errors.append(error("components.columns", "columns must be an array"))
        if not isinstance(components.get("actions"), list):
            errors.append(error("components.actions", "actions must be an array"))

    content = intent.get("content")
    content_title = content.get("title") if is_dict(content) else None
    content_body = content.get("body") if is_dict(content) else None

    if intent_type == "page.create":
        sections = intent.get("sections")
        if not isinstance(sections, list) or len(sections) == 0:
            errors.append(error("sections", "sections must be a non-empty array"))

    if intent_type == "form.create":
        if not is_non_empty_string(intent.get("formId")):
            errors.append(error("formId", "formId must be a non-empty string"))
        if is_dict(components) and isinstance(components.get("fields"), list):
            if len(components.get("fields")) == 0:
                errors.append(error("components.fields", "form intents must include at least one field"))

    if intent_type == "table.create":
        if not is_non_empty_string(intent.get("tableId")):
            errors.append(error("tableId", "tableId must be a non-empty string"))
        if is_dict(components) and isinstance(components.get("columns"), list):
            if len(components.get("columns")) == 0:
                errors.append(error("components.columns", "table intents must include at least one column"))

    if intent_type == "modal.open":
        if not is_non_empty_string(content_title):
            errors.append(error("content.title", "modal intents require content.title"))
        if not is_non_empty_string(content_body):
            errors.append(error("content.body", "modal intents require content.body"))

    if intent_type == "alert.show":
        severity = intent.get("severity")
        if not is_non_empty_string(severity) or severity not in ALLOWED_SEVERITIES:
            errors.append(error("severity", "severity must be info, warning, error, or success"))
        if not is_non_empty_string(content_body):
            errors.append(error("content.body", "alert intents require content.body"))

    if intent_type == "cta.request":
        if not is_non_empty_string(content_body):
            errors.append(error("content.body", "cta intents require content.body"))
        if is_dict(components) and isinstance(components.get("actions"), list):
            if len(components.get("actions")) == 0:
                errors.append(error("components.actions", "cta intents must include at least one action"))

    return errors


def main() -> None:
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError as exc:
        output = {"ok": False, "errors": [error("", f"Invalid JSON input: {exc}")]}
        json.dump(output, sys.stdout)
        sys.exit(0)

    intent = payload.get("intent") if isinstance(payload, dict) else None
    errors = validate_intent(intent)

    if errors:
        output = {"ok": False, "errors": errors}
        json.dump(output, sys.stdout)
        return

    output = {
        "ok": True,
        "errors": [],
        "schemaVersion": intent.get("schemaVersion"),
        "intent": intent,
    }
    json.dump(output, sys.stdout)


if __name__ == "__main__":
    main()
