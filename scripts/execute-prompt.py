#!/usr/bin/env python3
"""Emit a spec-scoped prompt execution context and log start event."""

import argparse
import json
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

MISSING_SPEC_ID_MESSAGE = (
    "Prompt execution blocked: no spec_id in objective-contract.json."
)


def load_objective_spec_id(path: Path) -> str:
    if not path.exists():
        raise SystemExit(MISSING_SPEC_ID_MESSAGE)
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        raise SystemExit(MISSING_SPEC_ID_MESSAGE)
    spec_id = data.get("spec_id")
    if not isinstance(spec_id, str) or not spec_id.strip():
        raise SystemExit(MISSING_SPEC_ID_MESSAGE)
    if spec_id.strip().startswith("<") and spec_id.strip().endswith(">"):
        raise SystemExit(MISSING_SPEC_ID_MESSAGE)
    return spec_id.strip()


def read_prompt_classification(path: Path) -> str:
    classification = None
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("Classification:"):
            classification = line.split(":", 1)[1].strip().lower()
            break
    if classification not in {"atomic", "decomposable"}:
        raise SystemExit("Prompt execution blocked: invalid prompt classification.")
    return classification


def emit_event(events_path: Path, spec_id: str, prompt_path: str, classification: str) -> None:
    event = {
        "event": "prompt_execution_started",
        "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "source": "execute-prompt.py",
        "spec_id": spec_id,
        "prompt_path": prompt_path,
        "classification": classification,
        "run_id": str(uuid.uuid4()),
    }
    with events_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event, separators=(",", ":")) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Emit prompt execution context")
    parser.add_argument("--prompt", required=True, help="Path to prompt artifact")
    args = parser.parse_args()

    prompt_path = Path(args.prompt)
    if not prompt_path.is_absolute():
        prompt_path = ROOT / prompt_path
    if not prompt_path.exists():
        raise SystemExit(f"Prompt file not found: {prompt_path}")

    spec_id = load_objective_spec_id(ROOT / "objective-contract.json")
    classification = read_prompt_classification(prompt_path)

    relative_prompt = str(prompt_path.relative_to(ROOT))
    emit_event(ROOT / "events.jsonl", spec_id, relative_prompt, classification)

    context = {
        "spec_id": spec_id,
        "prompt_path": relative_prompt,
        "classification": classification,
        "prompt_body": prompt_path.read_text(encoding="utf-8"),
    }
    sys.stdout.write(json.dumps(context, indent=2))


if __name__ == "__main__":
    main()
