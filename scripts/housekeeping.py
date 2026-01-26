#!/usr/bin/env python3
"""Non-interactive housekeeping: sync completed.md from checked tasks and optionally auto-push."""

from __future__ import annotations

import argparse
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Tuple

ROOT = Path(__file__).resolve().parent.parent
PENDING_NOTE = "(completed locally; pending push hash)"


def run(cmd: List[str]) -> Tuple[int, str, str]:
    proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
    return proc.returncode, proc.stdout.strip(), proc.stderr.strip()


def resolve_path(raw: str) -> Path:
    path = Path(raw)
    if path.is_absolute():
        return path
    return ROOT / path


def get_head_hash() -> str:
    code, out, _ = run(["git", "rev-parse", "HEAD"])
    if code != 0:
        raise SystemExit("Failed to resolve git HEAD hash.")
    return out.strip()


def normalize_summary(text: str) -> str:
    summary = text.strip()
    if summary.endswith(PENDING_NOTE):
        summary = summary[: -len(PENDING_NOTE)].rstrip()
    return summary


def extract_checked_tasks(todo_text: str) -> List[str]:
    tasks: List[str] = []
    for line in todo_text.splitlines():
        stripped = line.strip()
        if stripped.startswith("- [x] ") and PENDING_NOTE in stripped:
            tasks.append(normalize_summary(stripped[len("- [x] ") :]))
    return tasks


def extract_completed_summaries(completed_text: str) -> List[str]:
    summaries: List[str] = []
    for line in completed_text.splitlines():
        stripped = line.strip()
        if not stripped.startswith("- [x] "):
            continue
        # Format: - [x] YYYY-MM-DD — Summary (push <hash>) [evidence]
        if " — " in stripped:
            summary_part = stripped.split(" — ", 1)[1].strip()
            # Remove trailing evidence refs in brackets if present.
            if summary_part.endswith("]") and "[" in summary_part:
                summary_part = summary_part[: summary_part.rfind("[")].rstrip()
            # Remove trailing push hash annotation.
            if " (push " in summary_part:
                summary_part = summary_part.split(" (push ", 1)[0].rstrip()
            summaries.append(summary_part)
    return summaries


def update_todo_pending_notes(todo_text: str) -> str:
    lines: List[str] = []
    for line in todo_text.splitlines():
        if PENDING_NOTE in line:
            line = line.replace(PENDING_NOTE, "").rstrip()
        lines.append(line)
    return "\n".join(lines) + ("\n" if todo_text.endswith("\n") else "")


def sync_completed(todo_path: Path, completed_path: Path, push_hash: str, dry_run: bool) -> Tuple[int, List[str]]:
    todo_text = todo_path.read_text(encoding="utf-8") if todo_path.exists() else ""
    completed_text = completed_path.read_text(encoding="utf-8") if completed_path.exists() else "# Completed\n"

    checked_tasks = extract_checked_tasks(todo_text)
    existing = extract_completed_summaries(completed_text)

    new_entries: List[str] = []
    date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    for task in checked_tasks:
        if task in existing:
            continue
        entry = f"- [x] {date_str} — {task} (push {push_hash})"
        new_entries.append(entry)

    updated_completed = completed_text.rstrip("\n") + ("\n" if completed_text.strip() else "")
    if new_entries:
        updated_completed += "\n".join(new_entries) + "\n"

    updated_todo = update_todo_pending_notes(todo_text)

    if not dry_run:
        if new_entries:
            completed_path.write_text(updated_completed, encoding="utf-8")
        if updated_todo != todo_text:
            todo_path.write_text(updated_todo, encoding="utf-8")

    return len(new_entries), new_entries


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Housekeeping sync for completed tasks.")
    parser.add_argument("--todo", default="todo.md")
    parser.add_argument("--completed", default="completed.md")
    parser.add_argument("--push-hash", default=None)
    parser.add_argument("--auto-push", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)

    if args.auto_push:
        script = ROOT / "scripts" / "auto-push-if-safe.sh"
        if script.exists():
            code, out, err = run([str(script)])
            if out:
                print(out)
            if err:
                print(err)
        else:
            print("Auto-push skipped: scripts/auto-push-if-safe.sh not found.")

    push_hash = args.push_hash or get_head_hash()
    todo_path = resolve_path(args.todo)
    completed_path = resolve_path(args.completed)

    count, entries = sync_completed(todo_path, completed_path, push_hash, args.dry_run)
    if entries:
        for entry in entries:
            print(entry)
    else:
        print("No new completed entries to record.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
