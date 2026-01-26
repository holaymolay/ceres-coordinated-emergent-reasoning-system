# Iteration Backlog (Optional)

This directory is owned by the Hard Iteration Contract utility.
It is optional, off by default, and removable without impacting core CERES behavior.

## Owned Artifacts
- backlog.json: list of iteration items owned by this utility.
- progress.jsonl: append-only log of iteration runs.

## backlog.json format
Top-level JSON array of items:
- id (string)
- priority (int)
- title (string)
- spec_ref (path or id)
- acceptance_criteria_ref (path or anchor)
- passes (bool)
- evidence_refs (array of string)
- created_at (ISO-8601 UTC)

## progress.jsonl format
One JSON object per line:
- timestamp
- selected_id
- inputs_hash
- decision_rule_version
- result (pass|fail|partial)
- evidence_refs
- notes

## Rules
- This backlog is NOT the CERES task system.
- The utility never mutates governance state; it only writes these files.
- Removing this directory must not affect core CERES execution.
