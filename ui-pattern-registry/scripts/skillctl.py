#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import time
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Any

try:
    import jsonschema  # type: ignore
except Exception:  # pragma: no cover
    jsonschema = None  # type: ignore


class SkillctlError(Exception):
    pass


@dataclass(frozen=True)
class SkillRef:
    id: str
    version: str
    name: str
    path: Path


def _eprint(message: str) -> None:
    print(message, file=sys.stderr)


def _require_deps() -> None:
    missing = []
    if jsonschema is None:
        missing.append("jsonschema")
    if missing:
        _eprint(f"Missing dependencies: {', '.join(missing)}")
        _eprint("Set up a dedicated venv, e.g.:")
        _eprint("  scripts/setup-skillctl-venv.sh")
        _eprint("Then run:")
        _eprint("  scripts/skillctl <command> ...")
        raise SystemExit(2)


def _find_repo_root(start: Path) -> Path:
    current = start.resolve()
    for parent in [current, *current.parents]:
        if (parent / ".git").exists() or (parent / "AGENTS.md").exists():
            return parent
    raise SkillctlError(f"Could not locate repo root from: {start}")


def _skills_root(repo_root: Path) -> Path:
    skills_dir = repo_root / "skills"
    if not skills_dir.exists():
        raise SkillctlError(f"skills/ directory not found at: {skills_dir}")
    return skills_dir


def _iter_skill_dirs(skills_dir: Path) -> list[Path]:
    out: list[Path] = []
    for entry in sorted(skills_dir.iterdir(), key=lambda p: p.name):
        if not entry.is_dir():
            continue
        if entry.name.startswith("_"):
            continue
        if (entry / "skill.yaml").exists():
            out.append(entry)
    return out


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
        try:
            return json.loads(text)
        except Exception as e:
            raise SkillctlError(f"Unsupported flow value (must be JSON): {text}") from e
    if text.startswith('"') and text.endswith('"'):
        try:
            return json.loads(text)
        except Exception as e:
            raise SkillctlError(f"Invalid quoted string: {text}") from e
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
            raise SkillctlError("Tabs are not allowed in skill.yaml (use spaces).")
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
        raise SkillctlError(f"Unexpected indentation at line: {current_text}")

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
            raise SkillctlError(f"Invalid mapping entry (missing ':'): {i_text}")
        key, rest = i_text.split(":", 1)
        key = key.strip()
        if not key:
            raise SkillctlError(f"Empty key in mapping entry: {i_text}")
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


def _load_yaml(path: Path) -> dict[str, Any]:
    raw = path.read_text(encoding="utf-8")
    lines = _preprocess_yaml(raw)
    if not lines:
        raise SkillctlError(f"Empty YAML file: {path}")
    top_indent = lines[0][0]
    if top_indent != 0:
        raise SkillctlError(f"Top-level YAML must start at indent 0: {path}")
    parsed, next_index = _parse_block(lines, 0, 0)
    if next_index != len(lines):
        raise SkillctlError(f"Trailing content could not be parsed in: {path}")
    if not isinstance(parsed, dict):
        raise SkillctlError(f"Expected YAML mapping at {path}")
    return parsed  # type: ignore[return-value]


def _load_json(path: Path) -> Any:
    raw = path.read_text(encoding="utf-8")
    try:
        return json.loads(raw)
    except json.JSONDecodeError as e:
        raise SkillctlError(f"Invalid JSON at {path}: {e}") from e


def _load_contract_schema(skills_dir: Path) -> dict[str, Any]:
    schema_path = skills_dir / "_schema" / "skill.schema.json"
    if not schema_path.exists():
        raise SkillctlError(f"Contract schema missing: {schema_path}")
    schema = _load_json(schema_path)
    if not isinstance(schema, dict):
        raise SkillctlError(f"Invalid contract schema (expected JSON object): {schema_path}")
    return schema  # type: ignore[return-value]


def _json_pointer(err: Any) -> str:
    if not getattr(err, "path", None):
        return "/"
    parts = []
    for part in err.path:
        if isinstance(part, int):
            parts.append(str(part))
        else:
            parts.append(str(part).replace("~", "~0").replace("/", "~1"))
    return "/" + "/".join(parts)


def _validate_manifest(manifest: dict[str, Any], schema: dict[str, Any]) -> None:
    _require_deps()
    validator_cls = jsonschema.validators.validator_for(schema)
    validator = validator_cls(schema)
    errors = sorted(validator.iter_errors(manifest), key=lambda e: (list(e.path), e.message))
    if errors:
        lines = ["Manifest validation failed:"]
        for err in errors:
            lines.append(f"- {_json_pointer(err)}: {err.message}")
        raise SkillctlError("\n".join(lines))


def _safe_join(base_dir: Path, rel_path: str) -> Path:
    if rel_path.startswith("/"):
        raise SkillctlError(f"Absolute paths are not allowed: {rel_path}")
    if ".." in Path(rel_path).parts:
        raise SkillctlError(f"Parent path segments are not allowed: {rel_path}")
    candidate = (base_dir / rel_path).resolve()
    base_resolved = base_dir.resolve()
    if base_resolved != candidate and base_resolved not in candidate.parents:
        raise SkillctlError(f"Path escapes skill directory: {rel_path}")
    return candidate


def _resolve_skill_dir(repo_root: Path, target: str, allow_template: bool = True) -> Path:
    candidate = Path(target)
    if "/" in target or target.startswith("."):
        skill_dir = (repo_root / candidate).resolve() if not candidate.is_absolute() else candidate.resolve()
        if not skill_dir.exists():
            raise SkillctlError(f"Skill path not found: {skill_dir}")
        if not (skill_dir / "skill.yaml").exists():
            raise SkillctlError(f"skill.yaml not found under: {skill_dir}")
        if not allow_template and skill_dir.name.startswith("_"):
            raise SkillctlError("Template/internal skills cannot be targeted without explicit allowance")
        return skill_dir

    skills_dir = _skills_root(repo_root)
    for skill_dir in _iter_skill_dirs(skills_dir):
        manifest = _load_yaml(skill_dir / "skill.yaml")
        if manifest.get("id") == target:
            return skill_dir
    raise SkillctlError(f"Unknown skill id: {target}")


def _skill_ref_from_manifest(skill_dir: Path, manifest: dict[str, Any]) -> SkillRef:
    return SkillRef(
        id=str(manifest["id"]),
        version=str(manifest["version"]),
        name=str(manifest["name"]),
        path=skill_dir,
    )


def _canonical_json(obj: Any) -> str:
    return json.dumps(obj, separators=(",", ":"), sort_keys=True) + "\n"


def cmd_list(repo_root: Path, args: argparse.Namespace) -> int:
    skills_dir = _skills_root(repo_root)
    skills = []
    for skill_dir in _iter_skill_dirs(skills_dir):
        manifest = _load_yaml(skill_dir / "skill.yaml")
        skills.append(_skill_ref_from_manifest(skill_dir, manifest))

    if args.json:
        payload = [
            {"id": s.id, "name": s.name, "version": s.version, "path": str(s.path.relative_to(repo_root))}
            for s in skills
        ]
        sys.stdout.write(_canonical_json(payload))
        return 0

    for s in skills:
        sys.stdout.write(f"{s.id}\t{s.version}\t{s.name}\t{s.path.relative_to(repo_root)}\n")
    return 0


def cmd_describe(repo_root: Path, args: argparse.Namespace) -> int:
    skill_dir = _resolve_skill_dir(repo_root, args.target, allow_template=args.allow_template)
    manifest = _load_yaml(skill_dir / "skill.yaml")
    if args.json:
        sys.stdout.write(_canonical_json(manifest))
        return 0
    ref = _skill_ref_from_manifest(skill_dir, manifest)
    sys.stdout.write(f"id: {ref.id}\nname: {ref.name}\nversion: {ref.version}\npath: {ref.path.relative_to(repo_root)}\n")
    return 0


def _validate_skill_dir(repo_root: Path, skill_dir: Path, args: argparse.Namespace) -> None:
    skills_dir = _skills_root(repo_root)
    contract_schema = _load_contract_schema(skills_dir)
    manifest_path = skill_dir / "skill.yaml"
    manifest = _load_yaml(manifest_path)
    _validate_manifest(manifest, contract_schema)

    input_schema_rel = manifest["io"]["inputSchema"]
    output_schema_rel = manifest["io"]["outputSchema"]
    _load_json(_safe_join(skill_dir, input_schema_rel))
    _load_json(_safe_join(skill_dir, output_schema_rel))


def cmd_validate(repo_root: Path, args: argparse.Namespace) -> int:
    targets = []
    if args.all:
        targets = [str(p.relative_to(repo_root)) for p in _iter_skill_dirs(_skills_root(repo_root))]
    else:
        targets = args.targets

    failures: list[str] = []
    for target in targets:
        try:
            skill_dir = _resolve_skill_dir(repo_root, target, allow_template=args.allow_template)
            _validate_skill_dir(repo_root, skill_dir, args)
        except Exception as e:
            failures.append(f"{target}: {e}")

    if failures:
        _eprint("Validation failed:")
        for f in failures:
            _eprint(f"- {f}")
        return 1

    return 0


def cmd_run(repo_root: Path, args: argparse.Namespace) -> int:
    skill_dir = _resolve_skill_dir(repo_root, args.target, allow_template=args.allow_template)
    skills_dir = _skills_root(repo_root)
    contract_schema = _load_contract_schema(skills_dir)
    manifest = _load_yaml(skill_dir / "skill.yaml")
    _validate_manifest(manifest, contract_schema)
    skill_ref = _skill_ref_from_manifest(skill_dir, manifest)

    input_schema = _load_json(_safe_join(skill_dir, manifest["io"]["inputSchema"]))
    output_schema = _load_json(_safe_join(skill_dir, manifest["io"]["outputSchema"]))

    raw_input = Path(args.input).read_bytes() if args.input else sys.stdin.buffer.read()
    try:
        input_obj = json.loads(raw_input.decode("utf-8"))
    except Exception as e:
        raise SkillctlError(f"Input is not valid UTF-8 JSON: {e}") from e

    _require_deps()
    jsonschema.validate(instance=input_obj, schema=input_schema)

    runtime = manifest["runtime"]
    command = runtime["command"]
    timeout_ms = int(args.timeout_ms) if args.timeout_ms is not None else int(runtime.get("timeoutMs", 60000))
    runtime_cwd_rel = runtime.get("cwd", ".")
    cwd = _safe_join(skill_dir, runtime_cwd_rel)

    started = time.monotonic()
    proc = None
    stdout = b""
    stderr = b""
    exit_code: int | None = None
    status = "error"
    error_message: str | None = None

    try:
        proc = subprocess.run(
            command,
            cwd=str(cwd),
            input=_canonical_json(input_obj).encode("utf-8"),
            capture_output=True,
            timeout=timeout_ms / 1000.0,
            env={**os.environ},
        )
        stdout = proc.stdout
        stderr = proc.stderr
        exit_code = proc.returncode
        if proc.returncode != 0:
            raise SkillctlError(f"Skill exited with code {proc.returncode}")

        try:
            output_obj = json.loads(stdout.decode("utf-8"))
        except Exception as e:
            raise SkillctlError(f"Skill stdout is not valid JSON: {e}") from e

        jsonschema.validate(instance=output_obj, schema=output_schema)
        status = "success"
        normalized = _canonical_json(output_obj).encode("utf-8")
        if args.output:
            Path(args.output).write_bytes(normalized)
        else:
            sys.stdout.buffer.write(normalized)
    except Exception as e:
        error_message = str(e)
    finally:
        duration_ms = int((time.monotonic() - started) * 1000)
        if stderr:
            sys.stderr.buffer.write(stderr)
            if not stderr.endswith(b"\n"):
                sys.stderr.buffer.write(b"\n")

        report = {
            "event": "skill_run_report",
            "skill": {
                "id": skill_ref.id,
                "version": skill_ref.version,
                "path": str(skill_ref.path.relative_to(repo_root)),
            },
            "status": status,
            "durationMs": duration_ms,
            "exitCode": exit_code,
        }
        if error_message:
            report["error"] = error_message
        sys.stderr.write(_canonical_json(report))

    return 0 if status == "success" else 1


def _yaml_quote(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def _validate_skill_id(skill_id: str) -> None:
    if not re.fullmatch(r"[a-z][a-z0-9_]*(\.[a-z][a-z0-9_]*)*", skill_id):
        raise SkillctlError(
            "Invalid skill id (expected dot-namespace with snake segments), "
            "example: schema.validate_json"
        )


def _validate_skill_slug(slug: str) -> None:
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug):
        raise SkillctlError("Invalid skill slug (expected kebab-case), example: schema-validate-json")


def _render_skill_yaml(*, skill_id: str, name: str, version: str, description: str, spec_id: str) -> str:
    return "\n".join(
        [
            "apiVersion: skill/v1",
            "kind: Skill",
            "",
            f"id: {skill_id}",
            f"name: {_yaml_quote(name)}",
            f"version: {version}",
            f"description: {_yaml_quote(description)}",
            "",
            "governance:",
            f"  specId: {_yaml_quote(spec_id)}",
            "  oneSkillPerCommit: true",
            "  concepts: []",
            "  synchronizations: []",
            "",
            "runtime:",
            "  type: command",
            "  command:",
            "    - sh",
            "    - impl/run.sh",
            "  cwd: \".\"",
            "  timeoutMs: 60000",
            "",
            "io:",
            "  inputSchema: schemas/input.schema.json",
            "  outputSchema: schemas/output.schema.json",
            "  input:",
            "    transport: stdin",
            "    encoding: json",
            "  output:",
            "    transport: stdout",
            "    encoding: json",
            "",
            "determinism:",
            "  network: forbidden",
            "  time: forbidden",
            "  randomness: forbidden",
            "",
            "security:",
            "  access:",
            "    filesystem:",
            "      read: []",
            "      write: []",
            "    env:",
            "      read: []",
            "    subprocess:",
            "      allowed: false",
            "    network:",
            "      allowed: false",
            "",
            "observability:",
            "  logs:",
            "    format: jsonl",
            "    destination: stderr",
            "  runReport:",
            "    enabled: true",
            "",
            "x-notes: {}",
            "",
        ]
    )


def _render_spec_md(*, title: str, spec_id: str, skill_id: str, slug: str) -> str:
    return "\n".join(
        [
            f"Spec Title: {title}",
            f"Spec ID: {spec_id}",
            f"User Story: As an execution agent or CLI user, I need the Skill `{skill_id}` so it can be selected and executed deterministically without any LLM.",
            "",
            "Functional Requirements:",
            f"- Provide a Skill `{skill_id}` implemented under `skills/{slug}/`.",
            "- Define schema-defined JSON stdin/stdout contracts via `schemas/input.schema.json` and `schemas/output.schema.json`.",
            "",
            "Non-functional Requirements:",
            "- Deterministic: no network/time/randomness unless explicitly declared.",
            "- Stateless: no persistence outside declared filesystem write globs.",
            "",
            "Testing Plan:",
            "- Add offline fixtures under `fixtures/` and a smoke test under `tests/`.",
            "",
            "Security Constraints:",
            "- Declare all access in `skill.yaml:security.access` and default-deny network.",
            "",
        ]
    )


def cmd_scaffold(repo_root: Path, args: argparse.Namespace) -> int:
    skill_id = args.skill_id
    slug = args.slug
    _validate_skill_id(skill_id)
    _validate_skill_slug(slug)

    name = args.name if args.name is not None else skill_id
    description = args.description if args.description is not None else f"Scaffolded Skill package for {skill_id}."
    version = args.version if args.version is not None else "0.1.0"
    spec_id = args.spec_id if args.spec_id is not None else str(uuid.uuid4())

    skills_dir = _skills_root(repo_root)
    template_dir = skills_dir / "_template"
    if not template_dir.exists():
        raise SkillctlError(f"Skill template directory not found: {template_dir}")

    dest_dir = skills_dir / slug
    if dest_dir.exists():
        raise SkillctlError(f"Destination already exists: {dest_dir}")

    dest_dir.mkdir(parents=True, exist_ok=False)

    for rel_dir in ("schemas", "impl", "fixtures", "tests"):
        src = template_dir / rel_dir
        dst = dest_dir / rel_dir
        if not src.exists():
            raise SkillctlError(f"Template missing required directory: {src}")
        shutil.copytree(src, dst)

    (dest_dir / "skill.yaml").write_text(
        _render_skill_yaml(
            skill_id=skill_id,
            name=name,
            version=version,
            description=description,
            spec_id=spec_id,
        ),
        encoding="utf-8",
    )

    specs_dir = repo_root / "specs"
    specs_dir.mkdir(parents=True, exist_ok=True)
    spec_path = specs_dir / f"skill-{slug}-v1.md"
    if not spec_path.exists():
        spec_path.write_text(
            _render_spec_md(
                title=f"Skill {skill_id} v1 (Scaffold)",
                spec_id=spec_id,
                skill_id=skill_id,
                slug=slug,
            ),
            encoding="utf-8",
        )

    _eprint(f"Scaffolded Skill directory: {dest_dir.relative_to(repo_root)}")
    _eprint(f"Scaffolded Spec file: {spec_path.relative_to(repo_root)}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="skillctl")
    parser.add_argument(
        "--repo-root",
        help="Override repository root (default: auto-detect).",
        default=None,
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    p_list = subparsers.add_parser("list")
    p_list.add_argument("--json", action="store_true")
    p_list.set_defaults(func=cmd_list)

    p_describe = subparsers.add_parser("describe")
    p_describe.add_argument("target")
    p_describe.add_argument("--json", action="store_true")
    p_describe.add_argument("--allow-template", action="store_true", help="Allow targeting skills under skills/_*.")
    p_describe.set_defaults(func=cmd_describe)

    p_validate = subparsers.add_parser("validate")
    p_validate.add_argument("targets", nargs="*")
    p_validate.add_argument("--all", action="store_true")
    p_validate.add_argument("--allow-template", action="store_true", help="Allow targeting skills under skills/_*.")
    p_validate.set_defaults(func=cmd_validate)

    p_run = subparsers.add_parser("run")
    p_run.add_argument("target")
    p_run.add_argument("--input", help="Path to JSON input file (default: stdin).")
    p_run.add_argument("--output", help="Write output JSON to a file (default: stdout).")
    p_run.add_argument("--timeout-ms", type=int, default=None)
    p_run.add_argument("--allow-template", action="store_true", help="Allow targeting skills under skills/_*.")
    p_run.set_defaults(func=cmd_run)

    p_scaffold = subparsers.add_parser("scaffold")
    p_scaffold.add_argument("skill_id", help="New skill id (example: fs.hash_tree).")
    p_scaffold.add_argument("slug", help="New skill slug under skills/ (example: fs-hash-tree).")
    p_scaffold.add_argument("--name", default=None, help="Human-friendly name (defaults to skill_id).")
    p_scaffold.add_argument("--description", default=None, help="Short description for discovery.")
    p_scaffold.add_argument("--version", default=None, help="Initial semver version (default: 0.1.0).")
    p_scaffold.add_argument("--spec-id", default=None, help="Spec ID UUID (default: auto-generate).")
    p_scaffold.set_defaults(func=cmd_scaffold)

    return parser


def main(argv: list[str]) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    repo_root = Path(args.repo_root) if args.repo_root else _find_repo_root(Path.cwd())
    try:
        return int(args.func(repo_root, args))
    except SkillctlError as e:
        _eprint(str(e))
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
