#!/usr/bin/env python3
"""
Minimal Signals emitter (informational-only).
Accepts doctor findings + config state, emits CLI notices and appends to events.jsonl.
Non-authoritative: no actions, no blocking, no scheduling. Fails closed if workspace is missing.
"""
from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, TextIO

ALLOWED_SEVERITY = {"info", "warning", "critical"}
FORBIDDEN_FIELDS = {"action", "recommendation", "rank", "score", "priority", "auto_fix", "auto_migrate"}


def _timestamp(now: Optional[datetime] = None) -> str:
    dt = now or datetime.now(timezone.utc)
    return dt.isoformat().replace("+00:00", "Z")


def resolve_workspace(env: Optional[Dict[str, str]] = None) -> Path:
    env = env or os.environ
    if "CERES_WORKSPACE" in env:
        workspace = Path(env["CERES_WORKSPACE"])
    else:
        workspace = Path(".ceres/workspace")
    if not workspace.exists():
        raise FileNotFoundError(f"CERES workspace not found: {workspace}")
    return workspace


def _normalize_signal(
    raw: Dict[str, Any],
    *,
    now: Optional[datetime],
) -> Dict[str, Any]:
    forbidden = FORBIDDEN_FIELDS.intersection(raw.keys())
    if forbidden:
        raise ValueError(f"Forbidden fields present in signal: {sorted(forbidden)}")

    if "id" not in raw or "message" not in raw:
        raise ValueError("Signal must include 'id' and 'message'")

    severity = str(raw.get("severity", "info")).lower()
    if severity not in ALLOWED_SEVERITY:
        raise ValueError(f"Invalid severity '{severity}'")

    normalized = dict(raw)
    normalized["severity"] = severity
    normalized.setdefault("source", "signals")
    normalized.setdefault("constitutional_reference", "")
    normalized["timestamp"] = _timestamp(now)
    return normalized


def _augment_with_config(signals: List[Dict[str, Any]], config_state: Optional[Dict[str, Any]], now: Optional[datetime]) -> None:
    if not config_state:
        return
    if config_state.get("pattern_recall_enabled"):
        signals.append(
            {
                "id": "pattern_recall_enabled",
                "severity": "info",
                "source": "config",
                "constitutional_reference": "§13 Observational Memory non-authority",
                "message": "Pattern Recall / Observational Memory layer enabled (informational only).",
            }
        )


def _maybe_add_audit_overdue(
    signals: List[Dict[str, Any]],
    last_audit_at: Optional[str],
    now: Optional[datetime],
    overdue_days: int,
) -> None:
    if not last_audit_at:
        signals.append(
            {
                "id": "self_audit_overdue",
                "severity": "warning",
                "source": "signals",
                "constitutional_reference": "§5 Artifacts",
                "message": "Self-audit timestamp missing; audit is overdue.",
            }
        )
        return
    try:
        last_dt = datetime.fromisoformat(last_audit_at.replace("Z", "+00:00"))
    except Exception:
        signals.append(
            {
                "id": "self_audit_overdue",
                "severity": "warning",
                "source": "signals",
                "constitutional_reference": "§5 Artifacts",
                "message": "Self-audit timestamp unreadable; audit is overdue.",
            }
        )
        return
    now_dt = now or datetime.now(timezone.utc)
    delta_days = (now_dt - last_dt).days
    if delta_days >= overdue_days:
        signals.append(
            {
                "id": "self_audit_overdue",
                "severity": "warning",
                "source": "signals",
                "constitutional_reference": "§5 Artifacts",
                "message": f"Self-audit is overdue (last {delta_days} days ago).",
            }
        )


def emit_signals(
    findings: Iterable[Dict[str, Any]],
    *,
    config_state: Optional[Dict[str, Any]] = None,
    last_audit_at: Optional[str] = None,
    audit_overdue_days: int = 90,
    now: Optional[datetime] = None,
    env: Optional[Dict[str, str]] = None,
    out: Optional[TextIO] = None,
) -> List[Dict[str, Any]]:
    """
    Emit signals based on provided findings and config state.
    - Append to events.jsonl in CERES workspace.
    - Print CLI notices.
    - No side effects beyond append-only log.
    """
    workspace = resolve_workspace(env)
    out_stream = out or sys.stdout
    events_path = workspace / "events.jsonl"
    events_path.parent.mkdir(parents=True, exist_ok=True)

    raw_signals: List[Dict[str, Any]] = list(findings or [])
    _augment_with_config(raw_signals, config_state, now)
    _maybe_add_audit_overdue(raw_signals, last_audit_at, now, audit_overdue_days)

    normalized_signals: List[Dict[str, Any]] = [
        _normalize_signal(sig, now=now) for sig in raw_signals
    ]

    # Append-only log
    with events_path.open("a", encoding="utf-8") as fh:
        for sig in normalized_signals:
            fh.write(json.dumps(sig, sort_keys=True) + "\n")

    # CLI notices
    for sig in normalized_signals:
        out_stream.write(f"[{sig['severity']}] {sig['id']}: {sig['message']} (source: {sig['source']})\n")

    return normalized_signals
