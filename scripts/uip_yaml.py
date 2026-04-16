from __future__ import annotations

from pathlib import Path
from typing import Any, Tuple


class YamlError(Exception):
    pass


def _strip_yaml_comment(line: str) -> str:
    if "#" not in line:
        return line
    in_quote = False
    escaped = False
    out = []
    for char in line:
        if escaped:
            out.append(char)
            escaped = False
            continue
        if char == "\\":
            escaped = True
            out.append(char)
            continue
        if char in {"'", '"'}:
            in_quote = not in_quote
            out.append(char)
            continue
        if char == "#" and not in_quote:
            break
        out.append(char)
    return "".join(out)


def _preprocess_yaml(text: str) -> list[Tuple[int, str]]:
    lines: list[Tuple[int, str]] = []
    for raw in text.splitlines():
        if "\t" in raw:
            raise YamlError("Tabs are not allowed in YAML (use spaces).")
        line = _strip_yaml_comment(raw).rstrip()
        if not line.strip():
            continue
        indent = len(line) - len(line.lstrip(" "))
        lines.append((indent, line.lstrip(" ")))
    return lines


def _parse_scalar(value: str) -> Any:
    if value in {"null", "Null", "NULL", "~"}:
        return None
    if value in {"true", "True", "TRUE"}:
        return True
    if value in {"false", "False", "FALSE"}:
        return False
    if value.startswith(("'", '"')) and value.endswith(("'", '"')) and len(value) >= 2:
        return value[1:-1]
    try:
        if "." in value:
            return float(value)
        return int(value)
    except ValueError:
        return value


def _parse_block(lines: list[Tuple[int, str]], index: int, indent: int) -> Tuple[Any, int]:
    if index >= len(lines):
        return {}, index

    _, text = lines[index]
    if text.startswith("- "):
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
                if ":" in rest and not rest.lstrip().startswith(("'", '"')):
                    key, value = rest.split(":", 1)
                    key = key.strip()
                    if not key:
                        raise YamlError(f"Empty key in mapping entry: {rest}")
                    value = value.strip()
                    mapping: dict[str, Any] = {}
                    if value == "":
                        if i >= len(lines) or lines[i][0] <= indent:
                            mapping[key] = {}
                        else:
                            child_indent = lines[i][0]
                            child, i = _parse_block(lines, i, child_indent)
                            mapping[key] = child
                    else:
                        mapping[key] = _parse_scalar(value)

                    if i < len(lines) and lines[i][0] > indent:
                        child_indent = lines[i][0]
                        child, i = _parse_block(lines, i, child_indent)
                        if not isinstance(child, dict):
                            raise YamlError("List item mapping must be a mapping")
                        mapping.update(child)

                    items.append(mapping)
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
            raise YamlError(f"Invalid mapping entry (missing ':'): {i_text}")
        key, rest = i_text.split(":", 1)
        key = key.strip()
        if not key:
            raise YamlError(f"Empty key in mapping entry: {i_text}")
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


def load_yaml(path: Path) -> Any:
    raw = path.read_text(encoding="utf-8")
    lines = _preprocess_yaml(raw)
    if not lines:
        raise YamlError(f"Empty YAML file: {path}")
    top_indent = lines[0][0]
    if top_indent != 0:
        raise YamlError(f"Top-level YAML must start at indent 0: {path}")
    parsed, next_index = _parse_block(lines, 0, 0)
    if next_index != len(lines):
        leftover = ", ".join(line for _, line in lines[next_index: next_index + 3])
        raise YamlError(f"Trailing YAML content in {path}: {leftover}")
    return parsed
