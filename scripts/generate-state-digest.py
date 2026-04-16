#!/usr/bin/env python3
"""Generate a compact STATE.md digest from workspace artifacts.

Additive — does not replace authoritative files. Agents read the digest
first; consult source files when the digest is stale (hash mismatch) or
the task demands deeper context.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional


def resolve_workspace() -> Path:
    env = os.environ.get("CERES_WORKSPACE")
    if env:
        return Path(env)
    root = Path(__file__).resolve().parent.parent
    candidate = root / ".ceres" / "workspace"
    if candidate.is_dir():
        return candidate
    return root


def file_hash(path: Path) -> str:
    if not path.exists():
        return "missing"
    return hashlib.md5(path.read_bytes()).hexdigest()[:12]


def load_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}


def extract_section(text: str, heading: str) -> List[str]:
    lines: List[str] = []
    in_section = False
    for line in text.splitlines():
        if re.match(rf"^#{1,3}\s+{re.escape(heading)}", line, re.IGNORECASE):
            in_section = True
            continue
        if in_section:
            if re.match(r"^#{1,3}\s+", line):
                break
            stripped = line.strip()
            if stripped and stripped != "-":
                lines.append(stripped)
    return lines


def last_completed_entry(path: Path) -> Optional[str]:
    if not path.exists():
        return None
    entries = []
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped.startswith("- [x] ") and "YYYY-MM-DD" not in stripped:
            entries.append(stripped[6:])
    return entries[-1] if entries else None


def generate(workspace: Path) -> str:
    obj_path = workspace / "objective-contract.json"
    gap_path = workspace / "gap-ledger.json"
    todo_path = workspace / "todo.md"
    completed_path = workspace / "completed.md"
    memory_path = workspace / "memory.md"
    inbox_path = workspace / "todo-inbox.md"

    obj = load_json(obj_path)
    gaps = load_json(gap_path)

    todo_text = todo_path.read_text(encoding="utf-8") if todo_path.exists() else ""
    memory_text = memory_path.read_text(encoding="utf-8") if memory_path.exists() else ""

    spec_id = obj.get("spec_id", "(none)")
    obj_status = obj.get("status", "(none)")
    goal = obj.get("goal", "").strip() or "(not set)"

    gap_list = gaps.get("gaps", [])
    blocking = [g for g in gap_list if isinstance(g, dict) and g.get("blocking") and g.get("status") != "resolved"]
    open_gaps = [g for g in gap_list if isinstance(g, dict) and g.get("status") != "resolved"]

    current_focus = extract_section(todo_text, "Current Focus")
    decisions = extract_section(memory_text, "Decisions")
    risks = extract_section(memory_text, "Active Risks")

    last_done = last_completed_entry(completed_path)

    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    sources = {
        "objective-contract.json": file_hash(obj_path),
        "gap-ledger.json": file_hash(gap_path),
        "todo.md": file_hash(todo_path),
        "completed.md": file_hash(completed_path),
        "memory.md": file_hash(memory_path),
        "todo-inbox.md": file_hash(inbox_path),
    }

    lines = [
        "# STATE (auto-generated digest)",
        f"Generated: {ts}",
        "",
        f"Spec: {spec_id}",
        f"Objective status: {obj_status}",
        f"Goal: {goal}",
        f"Gaps: {len(open_gaps)} open, {len(blocking)} blocking",
        "",
    ]

    if current_focus:
        lines.append("## Current Focus")
        for item in current_focus[:10]:
            lines.append(item)
        lines.append("")

    if last_done:
        lines.append(f"Last completed: {last_done}")
        lines.append("")

    if decisions:
        lines.append("## Key Decisions")
        for item in decisions[:5]:
            lines.append(item)
        lines.append("")

    if risks:
        lines.append("## Active Risks")
        for item in risks[:5]:
            lines.append(item)
        lines.append("")

    lines.append("## Source Hashes")
    for name, h in sources.items():
        lines.append(f"- {name}: {h}")
    lines.append("")

    return "\n".join(lines)


def main() -> None:
    workspace = resolve_workspace()
    digest = generate(workspace)
    out_path = workspace / "STATE.md"
    out_path.write_text(digest, encoding="utf-8")
    print(f"STATE digest written to {out_path}")


if __name__ == "__main__":
    main()
