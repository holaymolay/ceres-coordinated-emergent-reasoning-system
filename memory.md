# Memory Ledger
Status: Canonical memory ledger. If conflict with `handover.md`, this file prevails.

## Decisions (authoritative)
- Preflight gate required before execution: `scripts/preflight.sh --mode execute`.
- Auto-push allowed when safe (post-commit hook runs `scripts/auto-push-if-safe.sh`).
- Canonical layer/repo docs live in `docs/canonical-layer-model.md` and `docs/repo-assignment.md`.
- Umbrella name is CERES — Coordinated Emergent Reasoning System; no parent framework above it.
- This repo is the CERES hub (coordination entrypoint); component repos remain independent.
- `CONSTITUTION.md` is binding; `PROMPTLOADER.md` is the bootstrap entry that points to it.
- Spec Elicitation runs after Objective Intake and before Objective Contract/Inference/Planning; it outputs `specs/elicitation/<spec-id>.md` and then stops.
- Prompt Debugger gates all intake before governance.
- Governed lifecycle: Objective Intake -> Spec Elicitation -> Objective Contract -> Inference (Gap Ledger) -> Planning (Task Plan -> `todo.md`) -> Controlled Prototyping -> Lock-In -> Execution -> Verification.
- Dual memory docs: `memory.md` is canonical; `handover.md` is export snapshot.

## Constraints & Assumptions
- Spec Elicitation must complete before inference, planning, or execution; `ready_for_planning` must be true and `blocking_unknowns` empty.
- Objective Contract must be committed for execution; blocking gaps must be resolved.
- No execution before a visible Task Plan exists in `todo.md`.
- Gap resolution requires evidence or explicit assumption with risk/expiry.
- No cross-repo changes without explicit coordination.
- Observability cannot be silenced; use `scripts/log_event.py` hooks.

## Active Risks / Unknowns
- None recorded; check `todo.md` for pending work.

## Artifact Index
- Spec Elicitation Record: `specs/elicitation/<spec-id>.md`
- Objective Contract: (not yet created)
- Gap Ledger: (not yet created)
- Task Plan: `todo.md`
- Prompt Debug Report: (not yet created)
- Completed Log: `completed.md`
- Handover Snapshot: `handover.md`

## Context Fragments (durable)
- `docs/canonical-layer-model.md` (canonical layer model)
- `docs/repo-assignment.md` (canonical repo assignment)
- `CONSTITUTION.md` (authority model + lifecycle + enforcement)
- `PROMPTLOADER.md` (bootstrap entry)
- `docs/visibility.md` (artifact roles and gates)
- `docs/execution-runtime.md` (runtime guardrails)
- `docs/routing.md` (component map)

## Handover Snapshot (for export)
### Current Focus
- Maintain CERES governance artifacts and hub documentation during reorganization.

### Recent Progress
- Added canonical docs for layer model and repo assignment.
- Added preflight gate script and auto-push safeguards.
- Installed handover auto-sync hooks and session watcher.
### Next Steps
- Complete Spec Elicitation Record, then populate Objective Contract and Gap Ledger when starting a new project.
- Use `scripts/preflight.sh --mode execute` before execution.
### Risks / Blockers
- None recorded.

## Change Log (chronological)
- 2026-01-05:
  - Established canonical memory ledger and handover export workflow.
  - Canonized layer model/repo assignment docs and added preflight + auto-push safeguards.
