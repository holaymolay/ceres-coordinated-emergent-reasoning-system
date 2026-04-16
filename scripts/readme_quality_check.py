#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

README_PATH = Path("README.md")
MAX_LINES = 200
MAX_EXCLAMATIONS = 0

REQUIRED_SECTIONS = [
    ("Who this is for", ["who this is for"]),
    ("Core problem", ["core problem", "problem"]),
    ("Solution", ["solution"]),
    ("Outcomes", ["outcomes", "what you get"]),
    ("Quick start", ["quick start"]),
    ("Non-goals", ["non-goals", "design philosophy"]),
]

BANNED_HEADINGS = ["overview", "introduction", "about"]


def fail(message: str) -> None:
    print(f"README QUALITY ERROR: {message}")
    sys.exit(1)


def load_lines() -> list[str]:
    if not README_PATH.exists():
        fail("README.md is missing.")
    return README_PATH.read_text(encoding="utf-8").splitlines()


def first_paragraph_after_title(lines: list[str]) -> tuple[str, int]:
    for i, line in enumerate(lines):
        if line.strip().startswith("# "):
            start = i + 1
            break
    else:
        fail("Missing top-level title (H1).")
    paragraph_lines = []
    end_line = start
    for j in range(start, len(lines)):
        if lines[j].strip() == "":
            end_line = j
            break
        paragraph_lines.append(lines[j].strip())
        end_line = j
    paragraph = " ".join(paragraph_lines).strip()
    return paragraph, end_line + 1


def count_sentence_endings(text: str) -> int:
    return sum(text.count(ch) for ch in [".", "?", "!"])


def collect_headings(lines: list[str]) -> list[str]:
    headings = []
    for line in lines:
        if line.startswith("## "):
            headings.append(line[3:].strip())
    return headings


def main() -> None:
    lines = load_lines()

    if len(lines) > MAX_LINES:
        fail(f"README.md exceeds {MAX_LINES} lines; reduce verbosity.")

    exclamations = "".join(lines).count("!")
    if exclamations > MAX_EXCLAMATIONS:
        fail(f"README.md uses {exclamations} exclamation points; limit is {MAX_EXCLAMATIONS}.")

    title_line = next((line for line in lines if line.strip()), "")
    if not title_line.startswith("# "):
        fail("Missing top-level title (H1) at the start of the file.")

    paragraph, end_line = first_paragraph_after_title(lines)
    if end_line > 10:
        fail("Value proposition must appear within the first 10 lines.")
    if count_sentence_endings(paragraph) != 1:
        fail("Value proposition must be a single sentence.")

    headings = collect_headings(lines)
    for heading in headings:
        lower = heading.lower()
        if any(banned in lower for banned in BANNED_HEADINGS):
            fail(f"Banned heading '{heading}' detected; use concrete section names.")

    cursor = -1
    for display, variants in REQUIRED_SECTIONS:
        match_index = -1
        for idx, heading in enumerate(headings):
            if idx <= cursor:
                continue
            if any(variant in heading.lower() for variant in variants):
                match_index = idx
                break
        if match_index == -1:
            fail(f"Missing required section: {display}. This section anchors README clarity.")
        cursor = match_index


if __name__ == "__main__":
    main()
