# CERES Visibility & Audit Standardization

These rules standardize how work is surfaced and audited across CERES.

## Files and Roles
- `todo-inbox.md`: raw intake (unordered bullets), structured sections; cleared by end-of-task sweep.
- Spec Elicitation Record: explicit decisions and unknowns from elicitation; required before inference/planning.
- `todo.md`: authoritative Task Plan (gated before execution). Sequenced `- [ ]` tasks with concept/phase/acceptance inline when helpful.
- `completed.md`: immutable audit log of finished tasks (`- [x]` with timestamp + push hash + evidence refs).
- `memory.md`: canonical memory ledger for decisions, constraints, and durable context.
- `handover.md`: export snapshot for context transfer; derived from `memory.md`.
- Gap Ledger: authoritative uncertainty/resolution queue (evidence-backed or explicit assumptions with expiry/risk).

## Gates & Flow
1) Intake -> Prompt Debugger -> governance.
2) Spec Elicitation produces the Spec Elicitation Record; no inference or planning before this completes.
3) Inference produces the Gap Ledger; resolve blocking gaps before planning.
4) Planning emits Task Plan -> `todo.md`; no execution before visible tasks exist.
5) Run preflight gate before execution: `scripts/preflight.sh --mode execute` (Prompt Debugger + lifecycle gate).
6) Execution works one task at a time; cannot add/reorder tasks.
7) On completion: update Gap Ledger (if relevant), move task to `completed.md` with timestamp/push hash, update `memory.md`; refresh `handover.md` with `scripts/export-handover.py` only when handing off context. (Auto-sync: `scripts/export-handover.py --watch` or `scripts/install-hooks.sh`; session helper: `scripts/start-session.sh`/`scripts/stop-session.sh`.)
8) Push and verify sync before closing the task: `scripts/push-and-verify.sh` (post-commit hook warns if ahead of origin).
9) Sweep `todo-inbox.md` at end of task cycles per governance rules.

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
