#!/usr/bin/env python3
"""
Pattern Recall / Observational Memory minimal hooks.

Non-authoritative observability extension guarded by feature flag and phase allowlist.
Outputs are informational-only and removable without affecting CERES behavior.
"""
from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

PATTERN_RECALL_ENABLED_ENV = "PATTERN_RECALL_ENABLED"
PATTERN_RECALL_ROOT_ENV = "PATTERN_RECALL_ROOT"

ALLOWED_PHASES = {"observe", "reflect", "pre-spec"}
FORBIDDEN_PHASES = {"plan", "decide", "execute", "arbitrate"}

FORBIDDEN_FIELDS = {
    "rank",
    "score",
    "recommendation",
    "priority",
    "weights",
    "likelihood",
    "rewrite",
    "auto_select",
    "auto_route",
}


def _bool_env(value: str) -> bool:
    return value.strip().lower() in {"1", "true", "yes", "on"}


def is_enabled(env: Optional[Dict[str, str]] = None) -> bool:
    env = env or os.environ
    return _bool_env(env.get(PATTERN_RECALL_ENABLED_ENV, "false"))


def _root(env: Optional[Dict[str, str]] = None) -> Path:
    env = env or os.environ
    override = env.get(PATTERN_RECALL_ROOT_ENV)
    if override:
        return Path(override)
    return Path(__file__).resolve().parent / "patterns"


def _normalize_phase(phase: Optional[str]) -> str:
    return (phase or "").strip().lower()


def _guard_phase(phase: Optional[str]) -> Tuple[bool, str]:
    normalized = _normalize_phase(phase)
    if normalized in ALLOWED_PHASES:
        return True, normalized
    return False, normalized


def _validate_fields(data: Dict[str, Any]) -> None:
    forbidden = FORBIDDEN_FIELDS.intersection(set(data.keys()))
    if forbidden:
        raise ValueError(f"Forbidden fields present: {sorted(forbidden)}")


def _timestamp() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _append_record(filename: str, record: Dict[str, Any], env: Optional[Dict[str, str]]) -> Path:
    root = _root(env)
    log_path = root / "logs"
    log_path.mkdir(parents=True, exist_ok=True)
    path = log_path / filename
    record = dict(record)
    record["recorded_at"] = record.get("recorded_at") or _timestamp()
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, sort_keys=True) + "\n")
    return path


def record_problem(
    problem_id: str,
    title: str,
    source: str,
    phase: str,
    provenance: Dict[str, Any],
    inputs: Optional[List[str]] = None,
    outcomes: Optional[List[str]] = None,
    extra: Optional[Dict[str, Any]] = None,
    env: Optional[Dict[str, str]] = None,
) -> Dict[str, Any]:
    env = env or os.environ
    if not is_enabled(env):
        return {"written": False, "reason": "pattern recall disabled"}
    ok, normalized_phase = _guard_phase(phase)
    if not ok:
        return {"written": False, "reason": f"phase '{normalized_phase}' not allowed"}

    record: Dict[str, Any] = {
        "id": problem_id,
        "title": title,
        "source": source,
        "phase": normalized_phase,
        "provenance": provenance,
        "inputs": inputs or [],
        "outcomes": outcomes or [],
    }
    if extra:
        _validate_fields(extra)
        record.update(extra)
    _validate_fields(record)
    path = _append_record("problems.ndjson", record, env)
    return {"written": True, "path": str(path)}


def record_attempt(
    attempt_id: str,
    problem_id: str,
    phase: str,
    summary: str,
    artifacts: Optional[List[str]] = None,
    outcome: Optional[str] = None,
    evidence: Optional[List[str]] = None,
    environment: Optional[Dict[str, Any]] = None,
    extra: Optional[Dict[str, Any]] = None,
    env: Optional[Dict[str, str]] = None,
) -> Dict[str, Any]:
    env = env or os.environ
    if not is_enabled(env):
        return {"written": False, "reason": "pattern recall disabled"}
    ok, normalized_phase = _guard_phase(phase)
    if not ok:
        return {"written": False, "reason": f"phase '{normalized_phase}' not allowed"}

    record: Dict[str, Any] = {
        "id": attempt_id,
        "problem_id": problem_id,
        "phase": normalized_phase,
        "summary": summary,
        "artifacts": artifacts or [],
        "outcome": outcome or "",
        "evidence": evidence or [],
        "environment": environment or {},
    }
    if extra:
        _validate_fields(extra)
        record.update(extra)
    _validate_fields(record)
    path = _append_record("attempts.ndjson", record, env)
    return {"written": True, "path": str(path)}


def record_classification(
    ref_id: str,
    phase: str,
    categories: Optional[List[str]] = None,
    tags: Optional[List[str]] = None,
    confidence: Optional[str] = None,
    extra: Optional[Dict[str, Any]] = None,
    env: Optional[Dict[str, str]] = None,
) -> Dict[str, Any]:
    env = env or os.environ
    if not is_enabled(env):
        return {"written": False, "reason": "pattern recall disabled"}
    ok, normalized_phase = _guard_phase(phase)
    if not ok:
        return {"written": False, "reason": f"phase '{normalized_phase}' not allowed"}

    record: Dict[str, Any] = {
        "ref_id": ref_id,
        "phase": normalized_phase,
        "categories": categories or [],
        "tags": tags or [],
    }
    if confidence:
        record["confidence"] = confidence
    if extra:
        _validate_fields(extra)
        record.update(extra)
    _validate_fields(record)
    path = _append_record("classifications.ndjson", record, env)
    return {"written": True, "path": str(path)}


def record_relation(
    from_id: str,
    to_id: str,
    relation_type: str,
    rationale: str,
    phase: str,
    evidence: Optional[List[str]] = None,
    extra: Optional[Dict[str, Any]] = None,
    env: Optional[Dict[str, str]] = None,
) -> Dict[str, Any]:
    env = env or os.environ
    if not is_enabled(env):
        return {"written": False, "reason": "pattern recall disabled"}
    ok, normalized_phase = _guard_phase(phase)
    if not ok:
        return {"written": False, "reason": f"phase '{normalized_phase}' not allowed"}

    record: Dict[str, Any] = {
        "from_id": from_id,
        "to_id": to_id,
        "relation_type": relation_type,
        "rationale": rationale,
        "phase": normalized_phase,
        "evidence": evidence or [],
    }
    if extra:
        _validate_fields(extra)
        record.update(extra)
    _validate_fields(record)
    path = _append_record("relations.ndjson", record, env)
    return {"written": True, "path": str(path)}


def _log_path(record_type: str, env: Optional[Dict[str, str]]) -> Path:
    filename_map = {
        "problem": "problems.ndjson",
        "attempt": "attempts.ndjson",
        "classification": "classifications.ndjson",
        "relation": "relations.ndjson",
    }
    filename = filename_map.get(record_type)
    if not filename:
        raise ValueError(f"Unknown record_type '{record_type}'")
    return _root(env) / "logs" / filename


def read_records(
    record_type: str,
    ids: Iterable[str],
    *,
    explicit_reference: bool,
    phase: str,
    env: Optional[Dict[str, str]] = None,
) -> List[Dict[str, Any]]:
    env = env or os.environ
    if not is_enabled(env):
        return []
    if not explicit_reference:
        raise ValueError("Explicit reference required to read pattern recall records.")
    ok, normalized_phase = _guard_phase(phase)
    if not ok:
        return []
    ids_set = set(ids or [])
    if not ids_set:
        raise ValueError("At least one ID must be provided for lookup.")

    path = _log_path(record_type, env)
    if not path.exists():
        return []

    matched: List[Dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                continue
            if _matches_ids(record, ids_set):
                matched.append(record)
    return matched


def _matches_ids(record: Dict[str, Any], ids: Iterable[str]) -> bool:
    ids_set = set(ids)
    for key in ("id", "problem_id", "attempt_id", "ref_id", "from_id", "to_id"):
        value = record.get(key)
        if value in ids_set:
            return True
    return False
