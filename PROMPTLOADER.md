# PROMPTLOADER.md
Status: Entry file · Canonical umbrella name locked

Umbrella name: **CERES — Coordinated Emergent Reasoning System** (final; no aliases above it).

## Read This First
- The binding source of truth is `CONSTITUTION.md`. Load and obey it before any action.
- This file exists to point agents to the Constitution and anchor the CERES name.


## Bootstrap for a New Project (minimal steps)
1. Place this `PROMPTLOADER.md` in the repo root and fetch `CONSTITUTION.md` from the same origin (https://github.com/holaymolay/ceres-coordinated-emergent-reasoning-system/blob/master/CONSTITUTION.md).
2. Pull the CERES components as needed (independent repos):
   - governance-orchestrator: https://github.com/holaymolay/governance-orchestrator
   - readme-spec-engine: https://github.com/holaymolay/readme-spec-engine
   - spec-compiler: https://github.com/holaymolay/spec-compiler
   - ui-constitution: https://github.com/holaymolay/ui-constitution
   - ui-pattern-registry: https://github.com/holaymolay/ui-pattern-registry
   - parallel-agent-runner (optional): https://github.com/holaymolay/parallel-agent-runner
   (Hub helper: `scripts/clone-components.sh` reads `repos.yaml` and clones any missing components.)
3. Use the hub Prompt Debugger before any governance/execution:
   - `prompt-debugger/cli.py --prompt-file task-inbox.md > /tmp/debug_report.yaml`
4. Enforce lifecycle gates before execution:
   - Task Plan must exist in `todo.md` (unchecked tasks).
   - Gap Ledger and Objective Contract present; assumptions explicit with risk/expiry.
   - Use governance gate: `scripts/enforce-lifecycle.py --todo todo.md --gap-ledger gap-ledger.json --prompt-report /tmp/debug_report.yaml` (inside governance-orchestrator).
5. Keep todo artifacts in the hub style: `todo-inbox.md`, `todo.md`, `completed.md`, `handover.md` (see hub docs for formatting).


## Quick Rules (see Constitution for full detail)
- Governed lifecycle only: Objective Contract → Inference (Gap Ledger) → Planning (Task Plan → `todo.md`) → Controlled Prototyping → Lock-In → Execution (PDCA) → Verification.
- Attention-bounded interaction: one bounded question per turn with rationale and visible state.
- No execution before a visible Task Plan exists in `todo.md`.
- All intake goes through the Prompt Debugger before governance; no silent fixes.
- No cross-repo changes without explicit coordination; execution obeys, governance decides.

If `CONSTITUTION.md` exists, it prevails over this file.
