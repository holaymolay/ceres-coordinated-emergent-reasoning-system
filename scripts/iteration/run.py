#!/usr/bin/env python3
"""Hard iteration contract utility (single-step, deterministic, optional)."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[2]
DECISION_RULE_VERSION = "1.0"
RULE_TEXT = "highest priority where passes=false; tie-break id ascending"


def parse_bool(value: str) -> bool:
    lowered = value.strip().lower()
    if lowered in {"true", "1", "yes", "on"}:
        return True
    if lowered in {"false", "0", "no", "off"}:
        return False
    raise argparse.ArgumentTypeError(f"Invalid boolean: {value}")


def load_backlog(path: Path) -> List[Dict[str, Any]]:
    if not path.is_file():
        raise SystemExit(f"Backlog not found: {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise SystemExit("Backlog must be a JSON array.")
    return data


def to_priority(value: Any) -> int:
    if isinstance(value, bool):
        return int(value)
    if isinstance(value, int):
        return value
    if isinstance(value, str):
        try:
            return int(value)
        except ValueError:
            return 0
    return 0


def candidate_key(item: Dict[str, Any]) -> tuple:
    priority = to_priority(item.get("priority", 0))
    item_id = item.get("id")
    if not isinstance(item_id, str):
        item_id = ""
    return (-priority, item_id)


def select_candidate(items: List[Dict[str, Any]]) -> tuple[List[Dict[str, Any]], Dict[str, Any] | None]:
    candidates = [item for item in items if not bool(item.get("passes", False))]
    ordered = sorted(candidates, key=candidate_key)
    selected = ordered[0] if ordered else None
    return ordered, selected


def compute_inputs_hash(items: List[Dict[str, Any]]) -> str:
    payload = json.dumps(items, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def build_record(
    selected: Dict[str, Any] | None,
    ordered: List[Dict[str, Any]],
    inputs_hash: str,
    evidence_refs: List[str],
    set_pass: bool,
) -> Dict[str, Any]:
    timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    selected_id = selected.get("id") if selected else None
    result = "pass" if set_pass and selected else "partial"
    top_order = [
        {"id": item.get("id"), "priority": to_priority(item.get("priority", 0))}
        for item in ordered[:5]
    ]
    return {
        "timestamp": timestamp,
        "selected_id": selected_id,
        "inputs_hash": inputs_hash,
        "decision_rule_version": DECISION_RULE_VERSION,
        "rule": RULE_TEXT,
        "ordered_candidates": top_order,
        "result": result,
        "evidence_refs": evidence_refs,
        "notes": "",
    }


def write_progress(path: Path, record: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, sort_keys=True))
        handle.write("\n")


def update_backlog(path: Path, items: List[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(items, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run one deterministic iteration step.")
    parser.add_argument("--backlog", default="scripts/iteration/backlog.json")
    parser.add_argument("--progress", default="scripts/iteration/progress.jsonl")
    parser.add_argument("--set-pass", type=parse_bool, default=False)
    parser.add_argument("--evidence-ref", action="append", default=[])
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--show-order", action="store_true")
    args = parser.parse_args(argv)

    backlog_path = Path(args.backlog)
    progress_path = Path(args.progress)

    items = load_backlog(backlog_path)
    ordered, selected = select_candidate(items)
    inputs_hash = compute_inputs_hash(items)

    record = build_record(
        selected=selected,
        ordered=ordered,
        inputs_hash=inputs_hash,
        evidence_refs=list(args.evidence_ref),
        set_pass=args.set_pass,
    )

    print(json.dumps(record, indent=2, sort_keys=True))

    if args.show_order and ordered:
        order_text = ", ".join(
            f"{item.get('id')}:{to_priority(item.get('priority', 0))}" for item in ordered[:5]
        )
        print(f"Order(top5): {order_text}", file=sys.stderr)

    if args.dry_run or not selected:
        return 0

    write_progress(progress_path, record)

    if args.set_pass:
        selected_id = selected.get("id")
        for item in items:
            if item.get("id") == selected_id:
                item["passes"] = True
                break
        update_backlog(backlog_path, items)

    return 0


if __name__ == "__main__":
    sys.exit(main())
