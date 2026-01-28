# Prompt: CERES Bootstrap Verification

Prompt ID: 9f0a66de-9b8b-4e0c-a4f1-7f4e6f0c7d1a
Classification: atomic
Status: approved
Owner: agent
Created: 2026-01-28T08:49:21Z
Last-Modified: 2026-01-28T08:49:21Z

## Intent
Verify that CERES is fully initialized and ready to accept a project prompt without any interactive setup.

## Constraints
- Non-interactive: do not ask questions.
- No code changes; only run verification commands and report status.
- Use FAST_START behavior (warnings only).

## Task Decomposition Guidance (decomposable only)
- N/A

## Prompt Body
You are executing a verification check. Do not ask questions.

Objective:
Confirm CERES is loaded and ready to accept a project prompt.

Steps:
1) Run `./.ceres/bin/autobootstrap` (non-blocking).
2) Run `.ceres/core/scripts/faststart-smoke.sh` (fallback to `scripts/faststart-smoke.sh` if present).
3) Run `./.ceres/bin/doctor` (fallback to `.ceres/core/scripts/doctor.py` if needed).
4) Run `./.ceres/bin/preflight --mode execute --prompt .ceres/workspace/todo-inbox.md --todo .ceres/workspace/todo.md --gap-ledger .ceres/workspace/gap-ledger.json --objective .ceres/workspace/objective-contract.json`.

Output:
- Report PASS/FAIL for each step with brief stdout/stderr notes.
- If any step fails, state that CERES is not ready and list missing paths or failures.
- If all pass, output exactly: "CERES READY — next prompt should describe the project."

## Validation Criteria
- All four steps executed.
- Readiness result clearly stated.
