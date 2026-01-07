#!/usr/bin/env python3
"""Allocate a spec_id after elicitation completes.

Idempotent: if a real spec_id already exists, it is preserved.
"""

import argparse
import json
import subprocess
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

PLACEHOLDER_VALUES = {"<spec-id>", "<spec_id>"}


def make_abs(value: str) -> Path:
    path = Path(value)
    if path.is_absolute():
        return path
    return ROOT / path


def resolve_elicitation(path: Path) -> Path:
    if path.is_dir():
        candidates = sorted(p for p in path.glob("*.md") if p.is_file())
        if not candidates:
            raise SystemExit(f"Spec Elicitation Record not found in {path}")
        if len(candidates) > 1:
            names = ", ".join(p.name for p in candidates)
            raise SystemExit(
                "Multiple Spec Elicitation Records found. "
                "Provide a single file or set --elicitation <path>. "
                f"Found: {names}"
            )
        return candidates[0]

    if not path.is_file():
        raise SystemExit(f"Spec Elicitation Record not found: {path}")

    return path


def parse_front_matter(text: str) -> tuple[dict, list[str], int]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise SystemExit("Spec Elicitation Record missing front matter (expected leading ---).")

    front_matter_lines = []
    end_index = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end_index = i
            break
        front_matter_lines.append(lines[i])

    if end_index is None:
        raise SystemExit("Spec Elicitation Record front matter not terminated (missing ---).")

    data: dict[str, object] = {}
    current_key: str | None = None

    for raw_line in front_matter_lines:
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" in line and not line.startswith("-"):
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip()
            current_key = None
            if value == "":
                data[key] = []
                current_key = key
            elif value in {"[]", "[ ]"}:
                data[key] = []
            elif value.lower() in {"true", "false"}:
                data[key] = value.lower() == "true"
            else:
                data[key] = value.strip("\"'")
        elif line.startswith("-") and current_key:
            item = line.lstrip("-").strip()
            if item:
                items = data.setdefault(current_key, [])
                if isinstance(items, list):
                    items.append(item)
        else:
            continue

    return data, lines, end_index


def is_placeholder(value: object) -> bool:
    if value is None:
        return True
    if not isinstance(value, str):
        return False
    trimmed = value.strip()
    if trimmed in PLACEHOLDER_VALUES:
        return True
    if trimmed.startswith("<") and trimmed.endswith(">"):
        return True
    return False


def validate_ready(data: dict) -> None:
    ready = data.get("ready_for_planning")
    if ready is not True:
        raise SystemExit("Spec Elicitation Record not ready_for_planning=true.")

    blocking = data.get("blocking_unknowns")
    if not isinstance(blocking, list):
        raise SystemExit("Spec Elicitation Record missing blocking_unknowns list in front matter.")
    if blocking:
        raise SystemExit("Spec Elicitation Record has blocking_unknowns; resolve before allocation.")


def update_front_matter(path: Path, lines: list[str], end_index: int, spec_id: str) -> bool:
    updated = False
    for i in range(1, end_index):
        if lines[i].lstrip().startswith("spec_id:"):
            if lines[i].strip() != f"spec_id: {spec_id}":
                lines[i] = f"spec_id: {spec_id}"
                updated = True
            break
    else:
        lines.insert(1, f"spec_id: {spec_id}")
        updated = True

    if updated:
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return updated


def update_objective(path: Path, spec_id: str) -> bool:
    if not path.is_file():
        raise SystemExit(f"Objective Contract not found: {path}")

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Failed to parse Objective Contract: {exc}")

    existing = data.get("spec_id")
    if existing and not is_placeholder(existing) and existing != spec_id:
        raise SystemExit(
            f"Objective Contract spec_id mismatch (found '{existing}', expected '{spec_id}')."
        )

    if existing == spec_id:
        return False

    data["spec_id"] = spec_id
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    return True


def event_exists(events_path: Path, spec_id: str) -> bool:
    if not events_path.is_file():
        return False
    with events_path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
            except json.JSONDecodeError:
                continue
            if data.get("event") == "spec_allocated" and data.get("spec_id") == spec_id:
                return True
    return False


def get_git_head() -> str | None:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
            check=False,
        )
    except OSError:
        return None

    if result.returncode != 0:
        return None

    value = (result.stdout or "").strip()
    return value or None


def emit_event(events_path: Path, spec_id: str, artifacts_updated: list[str]) -> None:
    event = {
        "event": "spec_allocated",
        "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "source": "allocate-spec-id.py",
        "spec_id": spec_id,
        "artifacts_updated": artifacts_updated,
        "run_id": str(uuid.uuid4()),
    }
    git_head = get_git_head()
    if git_head:
        event["git_head"] = git_head

    with events_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Allocate spec_id after elicitation")
    parser.add_argument(
        "--elicitation",
        default="specs/elicitation",
        help="Spec Elicitation path (default: specs/elicitation)",
    )
    parser.add_argument(
        "--objective",
        default="objective-contract.json",
        help="Objective Contract path (default: objective-contract.json)",
    )
    parser.add_argument(
        "--events",
        default="events.jsonl",
        help="Observability events JSONL (default: events.jsonl)",
    )

    args = parser.parse_args()
    events_path = make_abs(args.events)
    if events_path != ROOT / "events.jsonl":
        raise SystemExit("events must be ./events.jsonl at repo root")

    elicitation_path = resolve_elicitation(make_abs(args.elicitation))

    data, lines, end_index = parse_front_matter(elicitation_path.read_text(encoding="utf-8"))
    validate_ready(data)

    existing_spec = data.get("spec_id")
    allocated = False
    if is_placeholder(existing_spec):
        spec_id = str(uuid.uuid4())
        allocated = True
    else:
        spec_id = str(existing_spec).strip()

    updated_elicitation = update_front_matter(elicitation_path, lines, end_index, spec_id)
    updated_objective = update_objective(make_abs(args.objective), spec_id)

    artifacts_updated: list[str] = []
    if updated_elicitation:
        artifacts_updated.append(str(elicitation_path.relative_to(ROOT)))
    if updated_objective:
        artifacts_updated.append(str(make_abs(args.objective).relative_to(ROOT)))

    already_emitted = event_exists(events_path, spec_id)
    should_emit = not already_emitted and (allocated or not already_emitted)

    if should_emit:
        artifacts_updated.append(str(events_path.relative_to(ROOT)))
        emit_event(events_path, spec_id, artifacts_updated)
        if allocated:
            print(f"Allocated spec_id {spec_id}")
        else:
            print(f"Recorded spec_id {spec_id}")
    else:
        print(f"Spec_id already set: {spec_id}")


if __name__ == "__main__":
    main()
