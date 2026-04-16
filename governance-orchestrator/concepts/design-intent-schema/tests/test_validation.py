#!/usr/bin/env python3
import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
MODULE_PATH = ROOT / "concepts" / "design-intent-schema" / "handlers" / "intent" / "validate.py"


def load_validator():
    spec = importlib.util.spec_from_file_location("design_intent_validate", MODULE_PATH)
    if spec is None or spec.loader is None:
        print(f"Failed to load validator at {MODULE_PATH}", file=sys.stderr)
        raise SystemExit(1)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_fixture(name: str) -> dict:
    fixture_path = Path(__file__).resolve().parent / "fixtures" / name
    return json.loads(fixture_path.read_text(encoding="utf-8"))


def main() -> None:
    module = load_validator()
    validate = getattr(module, "validate_design_intent", None)
    require = getattr(module, "require_design_intent", None)
    if validate is None or require is None:
        print("Validator functions not found", file=sys.stderr)
        raise SystemExit(1)

    valid_intent = load_fixture("valid.intent.json")
    errors = validate(valid_intent)
    if errors:
        print("Expected valid intent to pass, got errors:", errors, file=sys.stderr)
        raise SystemExit(1)

    invalid_intent = load_fixture("invalid.intent.json")
    invalid_errors = validate(invalid_intent)
    if not invalid_errors:
        print("Expected invalid intent to fail validation", file=sys.stderr)
        raise SystemExit(1)

    try:
        require(invalid_intent)
    except ValueError:
        return
    print("Expected require_design_intent to raise on invalid intent", file=sys.stderr)
    raise SystemExit(1)


if __name__ == "__main__":
    main()
