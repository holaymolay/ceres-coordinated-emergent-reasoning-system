# Housekeeping Layer (Non-Interactive)

This layer handles routine, non-decision tasks so users are not asked to confirm obvious actions.
It is mandatory, deterministic, and non-authoritative.

## Purpose
- Eliminate user interruption for routine hygiene (push, completion logging, handover sync).
- Preserve governance by separating housekeeping from scope/decision changes.

## Responsibilities
- Auto-push changes when safe using `scripts/auto-push-if-safe.sh`.
- Update `completed.md` when tasks are marked complete in `todo.md` (append-only audit).
- Remove local "pending push hash" notes after a push hash is recorded.
- Keep housekeeping actions deterministic and reversible.

## Non-Goals
- Changing scope, creating tasks, or modifying governance decisions.
- Altering execution behavior beyond hygiene and logging.

## Required Behavior
- Do not ask the user to push or to record completed entries.
- Attempt auto-push; if blocked, record the reason in logs and continue without user interruption.
- Only sync `completed.md` from tasks already marked complete in `todo.md`.
- Use the marker `(completed locally; pending push hash)` on completed todo items before housekeeping sync; the marker is removed once the push hash is recorded.
- When configured, prune completed tasks from `todo.md` after they are recorded in `completed.md`.

## Tooling
- `scripts/housekeeping.py` for completion sync (use `--include-all` and `--prune-completed` for one-time cleanup).
- `scripts/auto-push-if-safe.sh` for safe auto-push.

## Safety
- Housekeeping must not modify tasks or specs.
- Housekeeping only touches `todo.md` (removing pending notes) and `completed.md` (append-only).
