# PROMPTLOADER.md
Status: Authoritative bootstrap entrypoint (non-interactive, deterministic).

Umbrella name: **CERES — Coordinated Emergent Reasoning System**.

## Non-Interactive Rule
Do not ask questions. Do not present options. Execute the bootstrap procedure and proceed.

## Procedure (run in order)
1) Fast init — install CERES core into `.ceres/core` using the first method that succeeds:

**a) Git submodule (preferred for repos already under git):**
```bash
git submodule add https://github.com/holaymolay/ceres-coordinated-emergent-reasoning-system.git .ceres/core 2>/dev/null || true
```

**b) Git clone (if submodule fails or git is available but repo is fresh):**
```bash
git clone --depth 1 https://github.com/holaymolay/ceres-coordinated-emergent-reasoning-system.git .ceres/core 2>/dev/null || true
```

**c) Tarball download (fallback if network + curl/wget available):**
```bash
mkdir -p .ceres/core
curl -fsSL https://github.com/holaymolay/ceres-coordinated-emergent-reasoning-system/releases/latest/download/ceres-fast.tar.gz -o /tmp/ceres-fast.tgz && tar -xzf /tmp/ceres-fast.tgz -C .ceres/core --strip-components 1
```

If `.ceres/core` already exists, skip step 1 entirely.

2) Initialize workspace/wrappers:

```bash
./.ceres/core/scripts/bootstrap-workspace.sh --root "$PWD"
```

3) Run autobootstrap (must succeed without questions):

```bash
./.ceres/bin/autobootstrap
```

4) Detect harness (non-blocking):

```bash
python3 ./.ceres/core/scripts/detect-harness.py 2>/dev/null || true
```

5) Ensure these exist (create/repair silently if missing):
- `.ceres/bin`
- either `.ceres/core` or root-level fallback scripts resolvable by `.ceres/bin/_paths.sh`
- `.ceres/workspace/todo-inbox.md`
- `.ceres/workspace/todo.md`
- `.ceres/workspace/completed.md`
- `.ceres/workspace/memory.md`
- `.ceres/workspace/handover.md`
- `.ceres/workspace/objective-contract.json`
- `.ceres/workspace/gap-ledger.json`
- `.ceres/workspace/specs/elicitation/elicitation.md`

6) Start session watcher (non-interactive):
- `./.ceres/bin/start-session`

7) Proceed directly to the first project prompt using:
- `prompts/plan.md` (Spec Elicitation + planning + execution start)

Verification prompt (when asked to confirm readiness):
- `prompts/prompt-ceres-verify.md`

Routing rule:
- If the user says "verify CERES is loaded/ready" (or equivalent), immediately execute `prompts/prompt-ceres-verify.md` with no questions.

## Required Defaults (FAST_START)
- execution_allowed = true
- enforcement = warn
- intake_required = auto-generate
- spec_elicitation = auto-generate-skeleton
- prompt_debugger = non-blocking
- gap_ledger = auto-append

## Constitutional Override
If `CONSTITUTION.md` exists, it must follow the non-interactive, auto-generate-and-proceed contract above.

CERES READY — next prompt should describe the project.
