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
from typing import Any, Dict


def main() -> None:
    parser = argparse.ArgumentParser(description="CERES event logger")
    parser.add_argument("--type", required=True, help="Event type (e.g., gate, stage, check)")
    parser.add_argument("--status", required=True, help="Status (e.g., pass, fail, info)")
    parser.add_argument("--message", required=True, help="Short message")
    parser.add_argument(
        "--context",
        help="Optional JSON context (string)",
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
            ctx = json.loads(args.context)
        except json.JSONDecodeError as exc:
            sys.stderr.write(f"Failed to parse context JSON: {exc}\n")
            sys.exit(1)

    event = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "type": args.type,
        "status": args.status,
        "message": args.message,
        "context": ctx,
    }

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event) + "\n")


if __name__ == "__main__":
    main()
