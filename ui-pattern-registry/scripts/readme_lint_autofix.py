#!/usr/bin/env python3
from __future__ import annotations

import argparse
import difflib
import re
import sys
from pathlib import Path

README_PATH = Path("README.md")
MAX_LINES = 200
MAX_EXCLAMATIONS = 0

CANONICAL_SECTIONS = [
    ("who", "Who this is for", ["who this is for"]),
    ("problem", "Core problem", ["core problem", "problem"]),
    ("solution", "Solution", ["solution"]),
    ("outcomes", "What you get", ["what you get", "outcomes"]),
    ("how", "How it works", ["how it works"]),
    ("quick", "Quick start", ["quick start"]),
    ("map", "Repository map", ["repository map"]),
    ("non-goals", "Design philosophy and non-goals", ["non-goals", "design philosophy"]),
]
CANONICAL_MAP = {key: canonical for key, canonical, _ in CANONICAL_SECTIONS}

BANNED_HEADINGS = ["overview", "introduction", "about"]


def fail(message: str) -> None:
    print(f"README LINT ERROR: {message}")
    sys.exit(1)


def load_lines() -> list[str]:
    if not README_PATH.exists():
        fail("README.md is missing.")
    return README_PATH.read_text(encoding="utf-8").splitlines()


def find_title(lines: list[str]) -> int:
    for idx, line in enumerate(lines):
        if line.strip().startswith("# "):
            return idx
    fail("Missing top-level title (H1).")
    return -1


def first_sentence_end_line(lines: list[str], start: int) -> int:
    for idx in range(start + 1, len(lines)):
        line = lines[idx]
        if line.strip() == "":
            break
        if any(ch in line for ch in [".", "?", "!"]):
            return idx + 1
    return -1


def collect_headings(lines: list[str]) -> list[str]:
    headings = []
    for line in lines:
        if line.startswith("## "):
            headings.append(line[3:].strip())
        if line.startswith("### "):
            headings.append(line[4:].strip())
    return headings


def normalize_heading(heading: str) -> tuple[str | None, str | None]:
    lower = heading.lower()
    for key, canonical, variants in CANONICAL_SECTIONS:
        if any(variant in lower for variant in variants):
            return key, canonical
    return None, None


def split_sections(lines: list[str]) -> tuple[list[str], list[tuple[str, list[str]]]]:
    preamble = []
    sections = []
    current_heading = None
    current_lines = []
    for line in lines:
        if line.startswith("## "):
            if current_heading is None:
                preamble = preamble or []
            else:
                sections.append((current_heading, current_lines))
            current_heading = line[3:].strip()
            current_lines = []
            continue
        if current_heading is None:
            preamble.append(line)
        else:
            current_lines.append(line)
    if current_heading is not None:
        sections.append((current_heading, current_lines))
    return preamble, sections


def trim_blank_lines(lines: list[str]) -> list[str]:
    trimmed = []
    blank = False
    for line in lines:
        if line.strip() == "":
            if blank:
                continue
            blank = True
            trimmed.append("")
            continue
        blank = False
        trimmed.append(line.rstrip())
    return trimmed


def check_readme(lines: list[str]) -> list[str]:
    errors = []
    if len(lines) > MAX_LINES:
        errors.append(f"README.md exceeds {MAX_LINES} lines.")

    exclamations = "".join(lines).count("!")
    if exclamations > MAX_EXCLAMATIONS:
        errors.append(
            f"README.md uses {exclamations} exclamation points; limit is {MAX_EXCLAMATIONS}."
        )

    title_index = find_title(lines)
    sentence_line = first_sentence_end_line(lines, title_index)
    if sentence_line == -1 or sentence_line > 10:
        errors.append("Value proposition sentence must end within the first 10 lines.")

    headings = collect_headings(lines)
    for heading in headings:
        lower = heading.lower()
        if any(banned in lower for banned in BANNED_HEADINGS):
            errors.append(f"Banned heading '{heading}' detected.")

    cursor = -1
    for key, canonical, variants in CANONICAL_SECTIONS:
        match_index = -1
        for idx, heading in enumerate(headings):
            if idx <= cursor:
                continue
            if any(variant in heading.lower() for variant in variants):
                match_index = idx
                break
        if match_index == -1:
            errors.append(f"Missing required section: {canonical}.")
        else:
            cursor = match_index
    return errors


def build_autofix(lines: list[str]) -> list[str]:
    preamble, sections = split_sections(lines)

    missing_keys = [key for key, _, _ in CANONICAL_SECTIONS]
    canonical_sections = {}
    extras = []

    for heading, content in sections:
        key, canonical = normalize_heading(heading)
        if key and key in missing_keys:
            missing_keys.remove(key)
            canonical_sections[key] = (canonical, content)
            continue
        if key and key in canonical_sections:
            extras.append((heading, content))
            continue
        lower = heading.lower()
        if any(banned in lower for banned in BANNED_HEADINGS) and missing_keys:
            key = missing_keys.pop(0)
            canonical_sections[key] = (CANONICAL_MAP[key], content)
            continue
        extras.append((heading, content))

    for key in list(missing_keys):
        canonical = CANONICAL_MAP[key]
        canonical_sections[key] = (canonical, ["TODO: Add content."])

    ordered_sections = []
    for key, canonical, _ in CANONICAL_SECTIONS:
        heading, content = canonical_sections[key]
        ordered_sections.append((heading, content))

    ordered_sections.extend(extras)

    output = []
    output.extend(preamble)
    if output and output[-1].strip() != "":
        output.append("")

    for heading, content in ordered_sections:
        output.append(f"## {heading}")
        output.extend(content)
        if output[-1].strip() != "":
            output.append("")

    return trim_blank_lines(output)


def main() -> None:
    parser = argparse.ArgumentParser(description="README lint and autofix.")
    parser.add_argument("--check", action="store_true", help="Validate README only.")
    parser.add_argument("--fix", action="store_true", help="Apply safe fixes.")
    args = parser.parse_args()

    if not args.check and not args.fix:
        fail("Specify --check or --fix.")

    lines = load_lines()

    if args.check:
        errors = check_readme(lines)
        if errors:
            fail(" ".join(errors))
        return

    fixed = build_autofix(lines)
    if fixed != lines:
        diff = difflib.unified_diff(
            lines,
            fixed,
            fromfile="README.md",
            tofile="README.md",
            lineterm="",
        )
        print("\n".join(diff))
        README_PATH.write_text("\n".join(fixed) + "\n", encoding="utf-8")
    else:
        print("README.md is already compliant.")


if __name__ == "__main__":
    main()
