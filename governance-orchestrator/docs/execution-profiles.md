# Execution Profiles

This document defines Safe Mode (default) and Fast Mode for enforcement scripts. The default behavior remains unchanged unless an explicit profile is set.

## Safe Mode (default)
- Enforces all invariant checks.
- Requires run records under `runs/YYYY-MM-DD/<run-id>.jsonl`.
- Requires Definition-of-Done artifacts (`completed.md`, `handover.md`, `CHANGELOG.md`) when code changes exist.

## Fast Mode
- Enforces one-Concept-per-commit and security rules.
- Skips run record requirement.
- Skips CHANGELOG enforcement (completed.md and handover.md remain required).
- Requires `FAST_MODE_SCOPE` to declare the active task/phase scope.
- Fast Mode must be logged in `handover.md` and the planner ledger with the active scope.
- Fast Mode expires when the declared scope no longer appears in `todo.md`.

## Activation
Set `EXECUTION_PROFILE=FAST` explicitly to enable Fast Mode. Any other value (or unset) is treated as Safe Mode.

## Logging
- Fast Mode usage must be logged in `handover.md` (include the phrase "Fast Mode").
- Mode is per-task and must be cleared after the task completes.
