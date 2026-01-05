# CERES Visibility & Audit Standardization

These rules standardize how work is surfaced and audited across CERES.

## Files and Roles
- `todo-inbox.md`: raw intake (unordered bullets), structured sections; cleared by end-of-task sweep.
- `todo.md`: authoritative Task Plan (gated before execution). Sequenced `- [ ]` tasks with concept/phase/acceptance inline when helpful.
- `completed.md`: immutable audit log of finished tasks (`- [x]` with timestamp + push hash + evidence refs).
- `handover.md`: current focus, recent progress, next steps, pending items.
- Gap Ledger: authoritative uncertainty/resolution queue (evidence-backed or explicit assumptions with expiry/risk).

## Gates & Flow
1) Intake → Prompt Debugger → governance.
2) Planning emits Task Plan → `todo.md`; no execution before visible tasks exist.
3) Execution works one task at a time; cannot add/reorder tasks.
4) On completion: update Gap Ledger (if relevant), move task to `completed.md` with timestamp/push hash, update `handover.md`.
5) Sweep `todo-inbox.md` at end of task cycles per governance rules.

## Assumptions
- Must be explicit: text + risk + expiry/revisit.
- Live in Gap Ledger until resolved or revoked.
- Cannot silently graduate to facts; require evidence or user confirmation.

## Formatting
- `todo.md`: `- [ ] Task summary` (imperative, scoped, testable); add short context inline when needed.
- `completed.md`: `- [x] YYYY-MM-DD — Task summary (push <hash>) [evidence refs]`.
- Gap Ledger entries tie to `task_id` and `gap_id` for traceability.

## Auditable Evidence
- File/line references, command outputs, test results, or user answers.
- Link evidence in Gap Ledger and `completed.md`.
- Log assumptions separately with risk/expiry.
