# PROMPTLOADER.md
Status: Authoritative bootstrap entrypoint (non-interactive, deterministic).

Umbrella name: **CERES — Coordinated Emergent Reasoning System**.

## Non-Interactive Rule
Do not ask questions. Do not present options. Execute the bootstrap procedure and proceed.

## Procedure (run in order)
1) Run autobootstrap (must succeed without questions):

```bash
curl -fsSL https://raw.githubusercontent.com/holaymolay/ceres-coordinated-emergent-reasoning-system/master/scripts/bootstrap-workspace.sh \
  -o /tmp/ceres-bootstrap.sh && bash /tmp/ceres-bootstrap.sh --components
./.ceres/bin/autobootstrap
```

2) Ensure these exist (create/repair silently if missing):
- `.ceres/core`
- `.ceres/bin`
- `.ceres/components`
- `.ceres/workspace/todo-inbox.md`
- `.ceres/workspace/todo.md`
- `.ceres/workspace/completed.md`
- `.ceres/workspace/memory.md`
- `.ceres/workspace/handover.md`
- `.ceres/workspace/objective-contract.json`
- `.ceres/workspace/gap-ledger.json`
- `.ceres/workspace/specs/elicitation/elicitation.md`

3) Start session watcher (non-interactive):
- `./.ceres/bin/start-session`

4) Proceed directly to the first project prompt using:
- `prompts/plan.md` (Spec Elicitation + planning + execution start)

Verification prompt (when asked to confirm readiness):
- `prompts/prompt-ceres-verify.md`

Routing rule:
- If the user says "verify CERES is loaded/ready" (or equivalent), immediately execute `prompts/prompt-ceres-verify.md` with no questions.

## Required Defaults (FAST_START)
- execution_allowed = true
- enforcement = warn
- intake_required = auto_generate
- spec_elicitation = auto_generate_skeleton
- prompt_debugger = non_blocking
- gap_ledger = auto_append

## Constitutional Override
If `CONSTITUTION.md` exists, it must follow the non-interactive, auto-generate-and-proceed contract above.

CERES READY — next prompt should describe the project.
