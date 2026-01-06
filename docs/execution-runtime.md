# CERES Execution Runtime Guardrails

This doc applies to the execution/runtime layer (agents that generate code). It enforces obedience to governance and evidence logging.

## Authority & Scope
- Execution obeys; it does not decide scope/routing. All scope and arbitration come from governance.
- Execution may only act on the active task from the Task Plan (`todo.md`).
- Execution cannot create or reorder tasks; propose changes via governance, which updates `todo.md` first.

## Required Inputs
- Spec Elicitation Record at `specs/elicitation/<spec-id>.md` with `ready_for_planning=true` and `blocking_unknowns` empty.
- Committed Objective Contract.
- Gap Ledger (with blockers resolved or explicitly deferred with assumptions).
- Task Plan in `todo.md` with the current task marked as in-progress.
- Prompt Debug Report attached to the originating request.
- Preflight gate run (`scripts/preflight.sh --mode execute`).
- Active phase set to `execution` or `correction` in `governance/inference-phases.yaml`.

## Required Outputs
- Code/artifact changes scoped to the current task only.
- Evidence logged back to Gap Ledger entries (files/lines, command outputs, test results).
- Completed tasks moved to `completed.md` with timestamp and push hash.
- Memory records written to `memory/records/*.json`; update `memory.md` summary when needed.
- Refresh `handover.md` via `scripts/export-handover.py` when exporting context.
- Push and verify sync before closing a task: `scripts/push-and-verify.sh` (auto-push may run via `scripts/auto-push-if-safe.sh`).

## Forbidden
- Changing scope, routing, or creating new tasks.
- Silent assumptions; all assumptions must be explicit with risk + expiry.
- Skipping verification; PDCA loop must run (tests/validation) or record why skipped.
- Muting observability/security hooks.
- Vibe coding: code generation or execution without an approved spec.

## PDCA Enforcement (execution side)
- Plan: accept the current task definition from `todo.md` (no edits here).
- Do: apply changes only within task scope.
- Check: run required tests/validation; capture evidence; reopen gaps if failures occur.
- Act: report outcomes; if assumptions were used, flag for governance follow-up.

## Evidence Logging Checklist
- Reference task_id and gap_id in commits/notes.
- Capture test/command output paths or logs.
- Update Gap Ledger status with evidence link.
- Update `completed.md` with timestamp, summary, and push hash.
