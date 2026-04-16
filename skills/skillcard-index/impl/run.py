#!/usr/bin/env python3

from __future__ import annotations

import json
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal


def eprint_json(event: str, payload: dict[str, Any]) -> None:
    sys.stderr.write(json.dumps({"event": event, **payload}, separators=(",", ":"), sort_keys=True) + "\n")


@dataclass(frozen=True)
class Issue:
    code: str
    message: str
    line: int | None = None

    def to_json(self) -> dict[str, Any]:
        obj: dict[str, Any] = {"code": self.code, "message": self.message}
        if self.line is not None:
            obj["line"] = int(self.line)
        return obj


Profile = Literal["compat", "anthropic-v1", "openai-codex-v1"]


def _split_frontmatter(markdown: str) -> tuple[str, list[Issue]]:
    lines = markdown.splitlines(keepends=True)
    if not lines:
        return "", [Issue(code="empty_input", message="SKILL.md content is empty")]

    if lines[0].strip("\r\n") != "---":
        return "", [Issue(code="missing_frontmatter", message="SKILL.md must start with YAML frontmatter '---'")]

    frontmatter_lines: list[str] = []
    end_index: int | None = None
    for i in range(1, len(lines)):
        if lines[i].strip("\r\n") == "---":
            end_index = i
            break
        frontmatter_lines.append(lines[i])

    if end_index is None:
        return "", [Issue(code="unterminated_frontmatter", message="YAML frontmatter must be terminated by '---'")]

    return "".join(frontmatter_lines), []


def _unquote_scalar(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and ((value[0] == value[-1] == '"') or (value[0] == value[-1] == "'")):
        return value[1:-1]
    return value


def _parse_frontmatter_scalars(frontmatter_text: str) -> tuple[dict[str, str], list[Issue], list[Issue]]:
    frontmatter: dict[str, str] = {}
    errors: list[Issue] = []
    warnings: list[Issue] = []

    for index, raw_line in enumerate(frontmatter_text.splitlines(), start=1):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue

        if ":" not in line:
            warnings.append(Issue(code="unparsed_line", message=f"Unrecognized frontmatter line: {raw_line!r}", line=index))
            continue

        key, value = line.split(":", 1)
        key = key.strip()
        value = _unquote_scalar(value)
        if not key:
            warnings.append(Issue(code="empty_key", message=f"Empty frontmatter key: {raw_line!r}", line=index))
            continue

        if key in frontmatter:
            errors.append(Issue(code="duplicate_key", message=f"Duplicate frontmatter key: {key}", line=index))
            continue

        frontmatter[key] = value.strip()

    return frontmatter, errors, warnings


def _validate_frontmatter(frontmatter: dict[str, str], profile: Profile) -> tuple[list[Issue], list[Issue]]:
    errors: list[Issue] = []
    warnings: list[Issue] = []

    name = frontmatter.get("name", "").strip()
    description = frontmatter.get("description", "").strip()

    if not name:
        errors.append(Issue(code="missing_name", message="Missing required frontmatter field: name"))
    if not description:
        errors.append(Issue(code="missing_description", message="Missing required frontmatter field: description"))

    if name:
        if profile in {"compat", "anthropic-v1"}:
            if not re.fullmatch(r"[a-z0-9-]+", name):
                errors.append(Issue(code="invalid_name_format", message="name must be hyphen-case: lowercase letters, digits, and hyphens only"))
            if name.startswith("-") or name.endswith("-") or "--" in name:
                errors.append(Issue(code="invalid_name_format", message="name cannot start/end with hyphen or contain consecutive hyphens"))
            if len(name) > 64:
                errors.append(Issue(code="name_too_long", message="name must be <= 64 characters"))
        else:
            if len(name) > 100:
                errors.append(Issue(code="name_too_long", message="name must be <= 100 characters"))

    if description:
        max_len = 500 if profile in {"compat", "openai-codex-v1"} else 1024
        if len(description) > max_len:
            errors.append(Issue(code="description_too_long", message=f"description must be <= {max_len} characters"))
        if profile in {"compat", "anthropic-v1"} and ("<" in description or ">" in description):
            errors.append(Issue(code="invalid_description", message="description cannot contain angle brackets (< or >)"))

    allowed_keys = {"name", "description", "license", "allowed-tools", "metadata"}
    unknown_keys = sorted(k for k in frontmatter.keys() if k not in allowed_keys)
    for key in unknown_keys:
        warnings.append(Issue(code="unknown_key", message=f"Unknown frontmatter key: {key}"))

    return errors, warnings


def _index_skillcards(root: Path, profile: Profile, max_results: int | None) -> dict[str, Any]:
    results: list[dict[str, Any]] = []
    for dirpath, dirnames, filenames in os.walk(root, topdown=True, followlinks=False):
        dirnames.sort()
        filenames.sort()
        if "SKILL.md" not in filenames:
            continue

        skill_path = Path(dirpath) / "SKILL.md"
        rel_path = skill_path.relative_to(root).as_posix()

        errors: list[Issue] = []
        warnings: list[Issue] = []
        frontmatter: dict[str, str] = {}

        try:
            markdown = skill_path.read_text(encoding="utf-8")
            frontmatter_text, split_errors = _split_frontmatter(markdown)
            frontmatter, parse_errors, parse_warnings = _parse_frontmatter_scalars(frontmatter_text)
            val_errors, val_warnings = _validate_frontmatter(frontmatter, profile)
            errors = split_errors + parse_errors + val_errors
            warnings = parse_warnings + val_warnings
        except Exception as e:
            errors = [Issue(code="read_error", message=str(e))]

        results.append(
            {
                "path": rel_path,
                "ok": len(errors) == 0,
                "frontmatter": dict(sorted(frontmatter.items())),
                "errors": [e.to_json() for e in errors],
                "warnings": [w.to_json() for w in warnings],
            }
        )

        if max_results is not None and len(results) >= max_results:
            break

    valid = sum(1 for r in results if r["ok"])
    invalid = len(results) - valid
    return {
        "root": str(root),
        "profile": profile,
        "total": len(results),
        "valid": valid,
        "invalid": invalid,
        "skillcards": results,
    }


def main() -> int:
    try:
        input_obj = json.load(sys.stdin)
        if not isinstance(input_obj, dict):
            raise ValueError("input must be a JSON object")

        root_raw = input_obj.get("root")
        if not isinstance(root_raw, str) or not root_raw:
            raise ValueError("root must be a non-empty string")

        profile_raw = input_obj.get("profile", "compat")
        if profile_raw not in {"compat", "anthropic-v1", "openai-codex-v1"}:
            raise ValueError("profile must be one of: compat, anthropic-v1, openai-codex-v1")
        profile: Profile = profile_raw

        max_results = input_obj.get("maxResults")
        if max_results is not None:
            if not isinstance(max_results, int) or max_results < 1:
                raise ValueError("maxResults must be a positive integer")

        root = Path(root_raw).resolve()
        if not root.exists() or not root.is_dir():
            raise ValueError("root must be an existing directory")

        output = _index_skillcards(root, profile, max_results)
        sys.stdout.write(json.dumps(output, separators=(",", ":"), sort_keys=True) + "\n")
        return 0
    except Exception as e:
        eprint_json("error", {"message": str(e)})
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
