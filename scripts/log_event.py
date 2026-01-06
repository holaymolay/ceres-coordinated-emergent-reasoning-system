#!/usr/bin/env python3
"""CERES observability helper.

Appends a JSONL event to ./logs/events.jsonl with a timestamp.
Use this as a lightweight hook from governance/execution stages.
"""
import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

PHASES = {"planning", "execution", "reflection", "correction"}


def parse_pattern_sequence(value: str) -> List[str]:
    try:
        data = json.loads(value)
    except json.JSONDecodeError:
        data = None

    if isinstance(data, list) and all(isinstance(item, str) for item in data):
        return data

    parts = [part.strip() for part in value.split(",")]
    return [part for part in parts if part]


def main() -> None:
    parser = argparse.ArgumentParser(description="CERES event logger")
    parser.add_argument("--type", required=True, help="Event type (e.g., gate, stage, check)")
    parser.add_argument("--status", required=True, help="Status (e.g., pass, fail, info)")
    parser.add_argument("--message", required=True, help="Short message")
    parser.add_argument("--phase", choices=sorted(PHASES), help="Active phase")
    parser.add_argument("--pattern", help="Active pattern name")
    parser.add_argument("--agent", help="Agent name")
    parser.add_argument("--task-id", help="Task identifier")
    parser.add_argument("--spec-id", help="Spec identifier")
    parser.add_argument("--synchronization-id", help="Synchronization identifier")
    parser.add_argument("--correction-count", type=int, help="Correction count")
    parser.add_argument(
        "--pattern-sequence",
        help="Pattern sequence (JSON array or comma-separated)",
    )
    parser.add_argument(
        "--context",
        help="Optional JSON context (object string)",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("logs/events.jsonl"),
        help="Output JSONL file",
    )
    args = parser.parse_args()

    ctx: Dict[str, Any] = {}
    if args.context:
        try:
            parsed = json.loads(args.context)
        except json.JSONDecodeError as exc:
            sys.stderr.write(f"Failed to parse context JSON: {exc}\n")
            sys.exit(1)
        if not isinstance(parsed, dict):
            sys.stderr.write("Context JSON must be an object.\n")
            sys.exit(1)
        ctx = parsed

    event: Dict[str, Any] = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "type": args.type,
        "status": args.status,
        "message": args.message,
    }

    if ctx:
        event["context"] = ctx
    if args.phase:
        event["phase"] = args.phase
    if args.pattern:
        event["pattern"] = args.pattern
    if args.agent:
        event["agent"] = args.agent
    if args.task_id:
        event["task_id"] = args.task_id
    if args.spec_id:
        event["spec_id"] = args.spec_id
    if args.synchronization_id:
        event["synchronization_id"] = args.synchronization_id
    if args.correction_count is not None:
        if args.correction_count < 0:
            sys.stderr.write("correction-count must be >= 0\n")
            sys.exit(1)
        event["correction_count"] = args.correction_count
    if args.pattern_sequence:
        sequence = parse_pattern_sequence(args.pattern_sequence)
        event["pattern_sequence"] = sequence

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event) + "\n")


if __name__ == "__main__":
    main()
