#!/usr/bin/env python3
"""Validate Reasoning Skills manifests and pipeline integrity."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any


class ValidationError(Exception):
    pass


def _eprint(message: str) -> None:
    print(message, file=sys.stderr)


def _find_repo_root(start: Path) -> Path:
    current = start.resolve()
    for parent in [current, *current.parents]:
        if (parent / "AGENTS.md").exists():
            return parent
    raise ValidationError(f"Could not locate repo root from: {start}")


def _strip_yaml_comment(line: str) -> str:
    in_single = False
    in_double = False
    out = []
    for ch in line:
        if ch == "'" and not in_double:
            in_single = not in_single
        elif ch == '"' and not in_single:
            in_double = not in_double
        if ch == "#" and not in_single and not in_double:
            break
        out.append(ch)
    return "".join(out)


def _parse_scalar(text: str) -> Any:
    lowered = text.lower()
    if lowered in {"null", "~"}:
        return None
    if lowered == "true":
        return True
    if lowered == "false":
        return False
    if text in {"[]", "{}"}:
        return [] if text == "[]" else {}
    if text.startswith("[") or text.startswith("{"):
        raise ValidationError(f"Unsupported flow value (must be JSON): {text}")
    if text.startswith('"') and text.endswith('"'):
        return text[1:-1]
    if text.startswith("'") and text.endswith("'") and len(text) >= 2:
        return text[1:-1].replace("''", "'")
    if text.isdigit() or (text.startswith("-") and text[1:].isdigit()):
        try:
            return int(text, 10)
        except Exception:
            pass
    return text


def _preprocess_yaml(text: str) -> list[tuple[int, str]]:
    out: list[tuple[int, str]] = []
    for raw in text.splitlines():
        if "\t" in raw:
            raise ValidationError("Tabs are not allowed (use spaces).")
        line = _strip_yaml_comment(raw).rstrip()
        if not line.strip():
            continue
        indent = len(line) - len(line.lstrip(" "))
        out.append((indent, line.lstrip(" ")))
    return out


def _parse_block(lines: list[tuple[int, str]], index: int, indent: int) -> tuple[Any, int]:
    if index >= len(lines):
        return {}, index
    current_indent, current_text = lines[index]
    if current_indent != indent:
        raise ValidationError(f"Unexpected indentation at line: {current_text}")

    if current_text.startswith("- "):
        items: list[Any] = []
        i = index
        while i < len(lines):
            i_indent, i_text = lines[i]
            if i_indent != indent or not i_text.startswith("- "):
                break
            rest = i_text[2:].strip()
            i += 1
            if rest == "":
                if i >= len(lines) or lines[i][0] <= indent:
                    items.append(None)
                else:
                    child_indent = lines[i][0]
                    child, i = _parse_block(lines, i, child_indent)
                    items.append(child)
            else:
                items.append(_parse_scalar(rest))
        return items, i

    mapping: dict[str, Any] = {}
    i = index
    while i < len(lines):
        i_indent, i_text = lines[i]
        if i_indent != indent or i_text.startswith("- "):
            break
        if ":" not in i_text:
            raise ValidationError(f"Invalid mapping entry (missing ':'): {i_text}")
        key, rest = i_text.split(":", 1)
        key = key.strip()
        if not key:
            raise ValidationError(f"Empty key in mapping entry: {i_text}")
        rest = rest.lstrip()
        i += 1
        if rest == "":
            if i >= len(lines) or lines[i][0] <= indent:
                mapping[key] = {}
            else:
                child_indent = lines[i][0]
                child, i = _parse_block(lines, i, child_indent)
                mapping[key] = child
        else:
            mapping[key] = _parse_scalar(rest)
    return mapping, i


def _load_yaml(path: Path) -> Any:
    raw = path.read_text(encoding="utf-8")
    lines = _preprocess_yaml(raw)
    if not lines:
        raise ValidationError(f"Empty YAML file: {path}")
    top_indent = lines[0][0]
    if top_indent != 0:
        raise ValidationError(f"Top-level YAML must start at indent 0: {path}")
    parsed, next_index = _parse_block(lines, 0, 0)
    if next_index != len(lines):
        leftover = ", ".join(line for _, line in lines[next_index:next_index + 3])
        raise ValidationError(f"Trailing YAML content in {path}: {leftover}")
    return parsed


def _validate_list_field(data: dict[str, Any], field: str, errors: list[str]) -> None:
    value = data.get(field)
    if not isinstance(value, list) or not value:
        errors.append(f"{field} must be a non-empty list")
        return
    for item in value:
        if not isinstance(item, str) or not item.strip():
            errors.append(f"{field} entries must be non-empty strings")
            break


def _validate_manifest(path: Path, data: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return [f"{path.name}: manifest must be a mapping"]

    required = {
        "skill_name",
        "skill_type",
        "description",
        "inputs",
        "transformations",
        "guarantees",
        "failure_conditions",
    }
    allowed = set(required)

    for key in data.keys():
        if key in allowed or key.startswith("x-"):
            continue
        errors.append(f"{path.name}: unexpected key '{key}'")

    for key in required:
        if key not in data:
            errors.append(f"{path.name}: missing required key '{key}'")

    skill_name = data.get("skill_name")
    if not isinstance(skill_name, str) or not skill_name:
        errors.append(f"{path.name}: skill_name must be a non-empty string")
    else:
        if not re.match(r"^[a-z][a-z0-9_]*$", skill_name):
            errors.append(f"{path.name}: skill_name has invalid format '{skill_name}'")
        if skill_name != path.stem:
            errors.append(
                f"{path.name}: skill_name '{skill_name}' must match filename '{path.stem}'"
            )

    skill_type = data.get("skill_type")
    if skill_type != "reasoning":
        errors.append(f"{path.name}: skill_type must be 'reasoning'")

    description = data.get("description")
    if not isinstance(description, str) or not description.strip():
        errors.append(f"{path.name}: description must be a non-empty string")

    _validate_list_field(data, "inputs", errors)
    _validate_list_field(data, "transformations", errors)
    _validate_list_field(data, "guarantees", errors)
    _validate_list_field(data, "failure_conditions", errors)

    return errors


def _validate_pipeline(
    path: Path,
    data: Any,
    manifest_names: set[str],
    strict: bool,
) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    if not isinstance(data, dict):
        return [f"{path.name}: pipeline must be a mapping"], warnings

    if set(data.keys()) != {"reasoning"}:
        extra = sorted(k for k in data.keys() if k != "reasoning")
        if extra:
            errors.append(f"{path.name}: unexpected keys {extra}")
        if "reasoning" not in data:
            errors.append(f"{path.name}: missing 'reasoning' list")
        if errors:
            return errors, warnings

    pipeline = data.get("reasoning")
    if not isinstance(pipeline, list) or not pipeline:
        return [f"{path.name}: reasoning must be a non-empty list"], warnings

    seen: set[str] = set()
    for name in pipeline:
        if not isinstance(name, str) or not name.strip():
            errors.append(f"{path.name}: pipeline entries must be non-empty strings")
            continue
        if name in seen:
            errors.append(f"{path.name}: duplicate pipeline entry '{name}'")
            continue
        seen.add(name)
        if name not in manifest_names:
            errors.append(f"{path.name}: pipeline entry '{name}' has no manifest")

    unused = sorted(manifest_names - seen)
    if unused:
        msg = f"Unused reasoning manifests: {', '.join(unused)}"
        if strict:
            errors.append(msg)
        else:
            warnings.append(msg)

    return errors, warnings


def _main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate Reasoning Skills manifests and pipeline integrity."
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Fail if any manifest is not referenced by the pipeline.",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Only output on errors.",
    )
    parser.add_argument(
        "--root",
        type=str,
        default=None,
        help="Repo root (defaults to searching from cwd).",
    )
    args = parser.parse_args()

    try:
        repo_root = Path(args.root).resolve() if args.root else _find_repo_root(Path.cwd())
    except ValidationError as exc:
        _eprint(str(exc))
        return 2

    reasoning_dir = repo_root / "skills" / "reasoning"
    if not reasoning_dir.exists():
        _eprint(f"Reasoning skills directory not found: {reasoning_dir}")
        return 2

    schema_path = reasoning_dir / "reasoning-skill.schema.yaml"
    pipeline_path = reasoning_dir / "pipeline.yaml"
    if not schema_path.exists():
        _eprint(f"Missing schema: {schema_path}")
        return 2
    if not pipeline_path.exists():
        _eprint(f"Missing pipeline: {pipeline_path}")
        return 2

    manifest_paths = sorted(
        [
            path
            for path in reasoning_dir.glob("*.yaml")
            if path.name not in {"pipeline.yaml", "reasoning-skill.schema.yaml"}
        ],
        key=lambda p: p.name,
    )

    errors: list[str] = []
    warnings: list[str] = []

    if not manifest_paths:
        errors.append("No reasoning manifests found.")
    manifest_names = {path.stem for path in manifest_paths}

    for path in manifest_paths:
        try:
            data = _load_yaml(path)
        except ValidationError as exc:
            errors.append(f"{path.name}: {exc}")
            continue
        errors.extend(_validate_manifest(path, data))

    try:
        pipeline = _load_yaml(pipeline_path)
    except ValidationError as exc:
        errors.append(f"{pipeline_path.name}: {exc}")
        pipeline = None
    if pipeline is not None:
        pipeline_errors, pipeline_warnings = _validate_pipeline(
            pipeline_path, pipeline, manifest_names, args.strict
        )
        errors.extend(pipeline_errors)
        warnings.extend(pipeline_warnings)

    if errors:
        _eprint("Reasoning Skills validation failed:")
        for err in errors:
            _eprint(f"- {err}")
        return 1

    if warnings and not args.quiet:
        for warning in warnings:
            _eprint(f"Warning: {warning}")

    if not args.quiet:
        print(
            f"OK: {len(manifest_paths)} manifests validated; "
            f"pipeline entries: {len(pipeline.get('reasoning', [])) if isinstance(pipeline, dict) else 0}."
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(_main())
