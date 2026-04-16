#!/usr/bin/env python3
import json
import re
import sys

ALLOWED_CAPABILITIES = {"utility", "baseline", "expressive", "custom"}
FORBIDDEN_PATTERNS = [
    ("INTENT_MARKUP_DETECTED", re.compile(r"<\s*(div|button|form|input|select|textarea|table|svg)\b", re.I)),
    ("INTENT_STYLE_DETECTED", re.compile(r"\bclassName\s*=")),
    ("INTENT_STYLE_DETECTED", re.compile(r"\bstyle\s*=\s*\"", re.I)),
]
TAILWIND_PATTERN = re.compile(r"\b(bg|text|flex|grid|px|py|mx|my|mt|mb|ml|mr|pt|pb|pl|pr|w|h)-[a-z0-9-]+\b", re.I)
CLASS_PATTERN = re.compile(r"\bclass(Name)?\s*=", re.I)


def emit(output):
    sys.stdout.write(json.dumps(output))


def main():
    raw = sys.stdin.read()
    if not raw.strip():
        emit({"ok": False, "errors": [{"code": "INPUT_EMPTY", "message": "Input is empty"}]})
        return 1
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as exc:
        emit({
            "ok": False,
            "errors": [{"code": "INPUT_PARSE_ERROR", "message": f"Invalid JSON: {exc}"}],
        })
        return 1

    errors = []
    if not isinstance(payload, dict):
        errors.append({"code": "INTENT_REQUIRED", "message": "Input must be an object"})
        emit({"ok": False, "errors": errors})
        return 1

    intent = payload.get("intent")
    if not isinstance(intent, dict):
        errors.append({"code": "INTENT_REQUIRED", "message": "intent must be an object"})

    capability = payload.get("capability") or "baseline"
    if capability not in ALLOWED_CAPABILITIES:
        errors.append({
            "code": "CAPABILITY_INVALID",
            "message": "capability must be one of utility, baseline, expressive, custom",
        })

    text_to_scan = payload.get("raw_output") or ""
    if not isinstance(text_to_scan, str):
        text_to_scan = ""
    for code, pattern in FORBIDDEN_PATTERNS:
        if pattern.search(text_to_scan):
            errors.append({"code": code, "message": "Forbidden markup or styling detected"})
            break
    if CLASS_PATTERN.search(text_to_scan) and TAILWIND_PATTERN.search(text_to_scan):
        errors.append({"code": "INTENT_TAILWIND_DETECTED", "message": "Tailwind classes detected"})

    if errors:
        emit({"ok": False, "errors": errors})
        return 1

    emit({"ok": True, "errors": [], "intent": intent, "capability": capability})
    return 0


if __name__ == "__main__":
    sys.exit(main())
