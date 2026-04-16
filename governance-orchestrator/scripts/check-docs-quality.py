#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROFILES = {"rich-human", "lean-reference", "strict-ci", "internal-notes"}
CALL_OUT_RE = re.compile(r"^\s*>\s*(NOTE|WARNING|TIP|EXAMPLE)\b", re.IGNORECASE)


def resolve_path(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


def read_text(path: Path) -> str:
    return resolve_path(path).read_text(encoding="utf-8")


def detect_profile(text: str) -> str:
    if not text.startswith("---\n"):
        return "rich-human"
    lines = text.splitlines()
    end_index = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end_index = i
            break
    if end_index is None:
        return "rich-human"
    for line in lines[1:end_index]:
        if line.strip().startswith("doc_profile:"):
            value = line.split(":", 1)[1].strip()
            return value
    return "rich-human"


def list_markdown_files(files: list[str]) -> list[Path]:
    if files:
        return [Path(path) for path in files if path.endswith(".md")]
    result = subprocess.run(
        ["git", "ls-files", "*.md"],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    return [Path(line) for line in result.stdout.splitlines() if line.strip()]


def run_markdownlint(path: Path, profile: str) -> bool:
    config = ROOT / f"docs/profiles/{profile}/.markdownlint.json"
    result = subprocess.run(
        ["markdownlint", "--config", str(config), str(path)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        sys.stderr.write(result.stdout)
        sys.stderr.write(result.stderr)
        return False
    return True


def collect_alerts(data: dict, path: Path) -> list[dict]:
    candidates = [
        str(path),
        path.as_posix(),
        str((ROOT / path).resolve()),
        str(path.resolve()),
    ]
    for key in candidates:
        if key in data:
            return data[key]
    alerts = []
    for value in data.values():
        if isinstance(value, list):
            alerts.extend(value)
    return alerts


def run_vale(path: Path, profile: str) -> tuple[bool, list[dict]]:
    if profile in {"lean-reference", "internal-notes"}:
        return True, []
    config = ROOT / f"docs/profiles/{profile}/vale/.vale.ini"
    result = subprocess.run(
        ["vale", "--output", "JSON", "--config", str(config), str(path)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    output = result.stdout.strip()
    if not output:
        return True, []
    try:
        data = json.loads(output)
    except json.JSONDecodeError:
        sys.stderr.write(result.stdout)
        sys.stderr.write(result.stderr)
        return False, []
    alerts = collect_alerts(data, path)
    return True, alerts


def format_alert(alert: dict) -> str:
    severity = str(alert.get("Severity", alert.get("severity", ""))).lower()
    message = alert.get("Message", alert.get("message", ""))
    line = alert.get("Line", alert.get("line", ""))
    return f"{severity or 'warning'}: line {line} {message}"


def main() -> int:
    parser = argparse.ArgumentParser(description="Structured Richness docs quality checks.")
    parser.add_argument("files", nargs="*", help="Optional markdown files to check.")
    args = parser.parse_args()
    markdown_files = list_markdown_files(args.files)
    include_internal = os.environ.get("DOCS_INCLUDE_INTERNAL_NOTES", "").lower() in {
        "1",
        "true",
        "yes",
    }
    failures = 0
    for path in markdown_files:
        text = read_text(path)
        profile = detect_profile(text)
        if profile not in PROFILES:
            sys.stderr.write(f"ERROR: {path} has unknown doc_profile '{profile}'.\n")
            failures += 1
            continue
        if profile == "internal-notes" and not include_internal:
            continue
        if profile == "lean-reference" and CALL_OUT_RE.search(text):
            sys.stderr.write(f"ERROR: {path} uses callouts under lean-reference.\n")
            failures += 1
            continue
        if not run_markdownlint(path, profile):
            failures += 1
            continue
        ok, alerts = run_vale(path, profile)
        if not ok:
            failures += 1
            continue
        if alerts:
            for alert in alerts:
                sys.stderr.write(f"{path}: {format_alert(alert)}\n")
        if profile == "strict-ci" and alerts:
            failures += 1
        if profile == "rich-human":
            has_error = any(
                str(alert.get("Severity", alert.get("severity", ""))).lower() == "error"
                for alert in alerts
            )
            if has_error:
                failures += 1
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
