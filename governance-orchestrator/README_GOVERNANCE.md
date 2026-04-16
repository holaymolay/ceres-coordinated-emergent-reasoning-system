# README governance

The README is a governed artifact generated from a spec, not free prose.
This document defines the boundaries between spec, generator, and enforcement.
It keeps README changes deterministic while preserving human review.
Follow these rules before any README change lands.

## Governed artifacts
- `README_SPEC.yaml` is the single source of truth for README content.
- `README.md` is generated from the spec by `readme-spec-engine`.
- This repository enforces structure and narrative quality; it does not generate content.

> NOTE: Never edit `README.md` directly. Update `README_SPEC.yaml`, regenerate externally, then enforce.

## Lifecycle
1. Draft or update `README_SPEC.yaml` with the desired narrative.
2. Run `readme-spec-engine` outside this repo to generate `README.md`.
3. Commit both files together.
4. Run README enforcement checks (lint + governance CI) to validate structure and compliance.

## Roles and boundaries
- Generation: `readme-spec-engine` (external project) turns specs into README content.
- Enforcement: this framework validates presence, structure, and governance of the generated README.
- Agents: must not free-write the README and must keep spec and README in sync.
- Humans: may author specs and review generated output before enforcement.

## Lifecycle Gates
- Run `scripts/enforce-lifecycle.py` before execution; it fails if `todo.md` has no unchecked tasks.
- Require a Prompt Debug Report from the umbrella `prompt-debugger/cli.py` for any intake (task-inbox/chat) before governance.
- Gap Ledger and Objective Contract must exist before planning; assumptions must be explicit with risk/expiry.
- Attention-bounded questioning: one bounded question per turn, tied to a Gap ID with rationale.
- Evidence-backed gap resolution only: evidence link, user answer, or explicit assumption with expiry/risk.

## Artifact Schemas
Located in the umbrella repo `schemas/`: Objective Contract, Gap Ledger, Task Plan (`todo.md` projection), Completed entry, Prompt Debug Report.

## Commands
- Prompt Debugger (from umbrella root): `prompt-debugger/cli.py --prompt-file task-inbox.md > /tmp/debug_report.yaml`
- Lifecycle gate (this repo, enforce todo template + logging): `scripts/enforce-lifecycle.py --todo todo.md --gap-ledger gap-ledger.json --prompt-report /tmp/debug_report.yaml --require-ceres-todo --log-helper ../scripts/log_event.py --task-id <id>`

- Observability hook: use umbrella `scripts/log_event.py` via `scripts/enforce-lifecycle.py --log-helper ../scripts/log_event.py --task-id <id>` to log gate outcomes.
- Optional template enforcement: `--require-ceres-todo` to ensure todo.md matches the CERES template header.

## Inference enforcement
- Run SEA first; then run inference to produce Gap Ledger before planning.
- Use lifecycle gate with `--require-gap-ledger --validate-gap-ledger` to block execution when Gap Ledger is missing/empty.
- Interrogation is one-question-at-a-time; record evidence/assumptions in the Gap Ledger.

## Interrogator / Resolver behavior
- Interrogator: one question at a time, tied to Gap ID and rationale; no compound or hypothetical questions; must update Gap Ledger status with answer/evidence or explicit assumption.
- Resolver: attempt `answerable_by_system` gaps using repo search/tests/static inspection; attach evidence links; unresolved blocking gaps stop planning.
- Gap Ledger: use `scripts/validate-gap-ledger.py` to ensure resolved gaps carry evidence or explicit assumptions.
