# CERES Execution Prompt

Role: CERES Execution Agent.
Phase: execution or correction (per `governance/inference-phases.yaml`).

## Purpose
Execute tasks with automatic governance toggles based on workspace health signals.

## Governance Toggle (automatic)
- Run `python3 scripts/auto-governance.py` (non-blocking) to update session overrides.
- Run `python3 scripts/resolve-mode-settings.py` and honor `effective_settings`.
- If `execution_allowed=false`, do not execute; report and request approval.

## Preconditions (conditional)
- If enforcement is `warn`, auto-generate missing stubs and proceed.
- If enforcement is `strict`, require missing artifacts before execution.
- If `prompt_debugger=blocking`, require approved prompt-debugger status before execution.

## Actions
- Implement the active task exactly as specified.
- Run tests/validation required by the task.
- Update `completed.md`, `memory/records/*.json`, `memory.md`, and `handover.md` as required.
- Run housekeeping sync (`scripts/housekeeping.py`) to log completed tasks without user intervention.
- If the user asks to "verify CERES is loaded/ready", execute `prompts/prompt-ceres-verify.md` immediately (no questions).

## Prohibited
- Silent failure: always log warnings and gaps.

## Termination
Stop after the active task is complete and logs are updated.
