#!/usr/bin/env python3
"""Rigor rule helpers (validation-only; no gating by default)."""

from __future__ import annotations

from typing import Dict, List


def validate_rigor_block(rigor: Dict) -> List[str]:
    errors: List[str] = []
    if not isinstance(rigor, dict):
        return ["rigor block must be an object"]

    verifiers = rigor.get("verifiers", [])
    if verifiers is not None and not isinstance(verifiers, list):
        errors.append("verifiers must be an array")
        verifiers = []

    verifier_ids = []
    for verifier in verifiers:
        if not isinstance(verifier, dict):
            errors.append("verifier entry must be an object")
            continue
        vid = verifier.get("id")
        if not isinstance(vid, str) or not vid.strip():
            errors.append("verifier.id must be a non-empty string")
        else:
            verifier_ids.append(vid)
        if not isinstance(verifier.get("description"), str) or not verifier.get("description"):
            errors.append(f"verifier {vid or '<unknown>'} missing description")
        if not isinstance(verifier.get("command"), str) or not verifier.get("command"):
            errors.append(f"verifier {vid or '<unknown>'} missing command")

    if len(set(verifier_ids)) != len(verifier_ids):
        errors.append("verifier ids must be unique")

    spec_map = rigor.get("spec_map", [])
    if spec_map is not None and not isinstance(spec_map, list):
        errors.append("spec_map must be an array")
        spec_map = []

    for mapping in spec_map:
        if not isinstance(mapping, dict):
            errors.append("spec_map entry must be an object")
            continue
        if not isinstance(mapping.get("spec_clause_id"), str) or not mapping.get("spec_clause_id"):
            errors.append("spec_map entry missing spec_clause_id")
        if not isinstance(mapping.get("verifier_id"), str) or not mapping.get("verifier_id"):
            errors.append("spec_map entry missing verifier_id")

    oracle = rigor.get("oracle")
    if oracle is not None and not isinstance(oracle, dict):
        errors.append("oracle must be an object")
    elif isinstance(oracle, dict):
        if not isinstance(oracle.get("script"), str) or not oracle.get("script"):
            errors.append("oracle.script must be a non-empty string")
        if not isinstance(oracle.get("description"), str) or not oracle.get("description"):
            errors.append("oracle.description must be a non-empty string")

    exploit_probe = rigor.get("exploit_probe")
    if exploit_probe is not None and not isinstance(exploit_probe, dict):
        errors.append("exploit_probe must be an object")
    elif isinstance(exploit_probe, dict):
        if not isinstance(exploit_probe.get("script"), str) or not exploit_probe.get("script"):
            errors.append("exploit_probe.script must be a non-empty string")
        if not isinstance(exploit_probe.get("description"), str) or not exploit_probe.get("description"):
            errors.append("exploit_probe.description must be a non-empty string")

    nondeterminism = rigor.get("nondeterminism")
    if nondeterminism is not None and not isinstance(nondeterminism, dict):
        errors.append("nondeterminism must be an object")
    elif isinstance(nondeterminism, dict):
        if not isinstance(nondeterminism.get("manifest_path"), str) or not nondeterminism.get("manifest_path"):
            errors.append("nondeterminism.manifest_path must be a non-empty string")

    return errors


def validate_spec_map(spec_clause_ids: List[str], verifier_ids: List[str], spec_map: List[Dict]) -> List[str]:
    errors: List[str] = []
    spec_set = set(spec_clause_ids)
    verifier_set = set(verifier_ids)

    mapped_specs = set()
    mapped_verifiers = set()

    for mapping in spec_map:
        spec_id = mapping.get("spec_clause_id")
        verifier_id = mapping.get("verifier_id")
        if spec_id not in spec_set:
            errors.append(f"spec_map refers to unknown spec clause: {spec_id}")
        else:
            mapped_specs.add(spec_id)
        if verifier_id not in verifier_set:
            errors.append(f"spec_map refers to unknown verifier: {verifier_id}")
        else:
            mapped_verifiers.add(verifier_id)

    missing_specs = spec_set - mapped_specs
    missing_verifiers = verifier_set - mapped_verifiers
    if missing_specs:
        errors.append(f"spec clauses missing verifiers: {', '.join(sorted(missing_specs))}")
    if missing_verifiers:
        errors.append(f"verifiers missing spec mapping: {', '.join(sorted(missing_verifiers))}")

    return errors


def require_nondeterminism_manifest(task_meta: Dict, nondeterminism: Dict | None) -> List[str]:
    errors: List[str] = []
    if not isinstance(task_meta, dict):
        return ["task_meta must be an object"]
    if task_meta.get("networked") is True:
        if not isinstance(nondeterminism, dict):
            errors.append("nondeterminism manifest required for networked tasks")
        elif not isinstance(nondeterminism.get("manifest_path"), str) or not nondeterminism.get("manifest_path"):
            errors.append("nondeterminism.manifest_path required for networked tasks")
    return errors
