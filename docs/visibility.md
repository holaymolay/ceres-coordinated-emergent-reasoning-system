# CERES Visibility & Audit Standardization

These rules standardize how work is surfaced and audited across CERES.

## Files and Roles
- `todo-inbox.md`: raw intake (unordered bullets), structured sections; cleared by end-of-task sweep.
- Spec Elicitation Record: `specs/elicitation/<spec-id>.md` with front matter (`ready_for_planning`, `blocking_unknowns`).
- `todo.md`: authoritative Task Plan (gated before execution). Sequenced `- [ ]` tasks with concept/phase/acceptance inline when helpful.
- Prompt Artifacts: `prompts/prompt-<slug>.md` (long-form prompts referenced from `todo.md`; immutable during execution).
- `completed.md`: immutable audit log of finished tasks (`- [x]` with timestamp + push hash + evidence refs).
- `memory/records/*.json`: canonical typed memory records (schema-enforced).
- `memory.md`: human-readable memory summary derived from records.
- `handover.md`: export snapshot for context transfer; derived from `memory.md`.
- `ceres.policy.yaml`: macro policy knobs (human-editable) validated by `scripts/policy_guard.py`.
- Gap Ledger: authoritative uncertainty/resolution queue (evidence-backed or explicit assumptions with expiry/risk).

## Gates & Flow
1) Intake -> Prompt Debugger -> governance.
2) Spec Elicitation produces the Spec Elicitation Record; `ready_for_planning` must be true and `blocking_unknowns` empty.
3) Phase enforcement applies per `governance/inference-phases.yaml` and `AGENTS.md`.
4) Inference produces the Gap Ledger; resolve blocking gaps before planning.
5) Planning emits Task Plan -> `todo.md`; no execution before visible tasks exist.
   Long-form prompts live in `prompts/prompt-<slug>.md` and are referenced from tasks instead of embedded.
6) Run preflight gate before execution: `scripts/preflight.sh --mode execute` (Prompt Debugger + lifecycle gate).
7) Execution works one task at a time; cannot add/reorder tasks.
8) On completion: update Gap Ledger (if relevant), move task to `completed.md` with timestamp/push hash, update memory records + `memory.md`; refresh `handover.md` with `scripts/export-handover.py` only when handing off context. Housekeeping is non-interactive; use `scripts/housekeeping.py` to sync completed entries. (Auto-sync: `scripts/export-handover.py --watch` or `scripts/install-hooks.sh`; session helper: `scripts/start-session.sh`/`scripts/stop-session.sh`.)
9) Push and verify sync before closing the task: `scripts/push-and-verify.sh` (post-commit hook warns if ahead of origin).
10) Sweep `todo-inbox.md` at end of task cycles per governance rules.

## Assumptions
- Must be explicit: text + risk + expiry/revisit.
- Live in Gap Ledger until resolved or revoked.
- Cannot silently graduate to facts; require evidence or user confirmation.

## Formatting
- `todo.md`: `- [ ] Task summary` (imperative, scoped, testable); add short context inline when needed.
- `todo.md` prompt reference: `- [ ] Execute prompt: prompts/prompt-<slug>.md` with outcome line.
- `completed.md`: `- [x] YYYY-MM-DD — Task summary (push <hash>) [evidence refs]`.
- Gap Ledger entries tie to `task_id` and `gap_id` for traceability.

## Auditable Evidence
- File/line references, command outputs, test results, or user answers.
- Link evidence in Gap Ledger and `completed.md`.
- Log assumptions separately with risk/expiry.
