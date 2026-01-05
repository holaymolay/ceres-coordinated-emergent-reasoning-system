# CERES Execution Runtime Guardrails

This doc applies to the execution/runtime layer (agents that generate code). It enforces obedience to governance and evidence logging.

## Authority & Scope
- Execution obeys; it does not decide scope/routing. All scope and arbitration come from governance.
- Execution may only act on the active task from the Task Plan (`todo.md`).
- Execution cannot create or reorder tasks; propose changes via governance, which updates `todo.md` first.

## Required Inputs
- Committed Objective Contract.
- Gap Ledger (with blockers resolved or explicitly deferred with assumptions).
- Task Plan in `todo.md` with the current task marked as in-progress.
- Prompt Debug Report attached to the originating request.

## Required Outputs
- Code/artifact changes scoped to the current task only.
- Evidence logged back to Gap Ledger entries (files/lines, command outputs, test results).
- Completed tasks moved to `completed.md` with timestamp and push hash.
- Handover notes updated with current focus and next steps.

## Forbidden
- Changing scope, routing, or creating new tasks.
- Silent assumptions; all assumptions must be explicit with risk + expiry.
- Skipping verification; PDCA loop must run (tests/validation) or record why skipped.
- Muting observability/security hooks.

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
