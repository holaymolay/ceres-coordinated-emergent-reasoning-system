# PROMPTLOADER.md
Status: Entry file · Canonical umbrella name locked

Umbrella name: **CERES — Coordinated Emergent Reasoning System** (final; no aliases above it).

## Read This First
- The binding source of truth is `CONSTITUTION.md`. Load and obey it before any action.
- This file exists to point agents to the Constitution and anchor the CERES name.

## Spec Elicitation (mandatory)
- Capture Objective Intake first (raw prompt or `todo-inbox.md`).
- Run the CERES Spec Elicitation Agent (SEA) before Objective Contract, Inference, or Planning.
- SEA instructions: `docs/sea.md`; artifact template: `templates/elicitation/elicitation.md`.
- SEA is read-only; outputs a single elicitation artifact then stops.

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
   - `prompt-debugger/cli.py --prompt-file todo-inbox.md > /tmp/debug_report.yaml`
4. Run the combined preflight gate before execution (Prompt Debugger + lifecycle gate):
   - `scripts/preflight.sh --mode execute --prompt todo-inbox.md --gap-ledger gap-ledger.json --objective objective-contract.json`
   - Initialize required artifacts if missing: `scripts/init-artifacts.sh`.
   - Task Plan must exist in `todo.md` (unchecked tasks).
   - Gap Ledger and Objective Contract present; assumptions explicit with risk/expiry.
5. Keep todo artifacts in the hub style: `todo-inbox.md`, `todo.md`, `completed.md`, `memory.md`, `handover.md` (see hub docs for formatting).
   - `memory.md` is canonical; `handover.md` is an export snapshot for context transfer.
   - Generate handover snapshot with `scripts/export-handover.py` when needed.
   - Auto-sync option: `scripts/export-handover.py --watch` or `scripts/install-hooks.sh`.
   - Session helper: `scripts/start-session.sh` (starts watch) and `scripts/stop-session.sh` (stops watch).
   - Start each LLM session by running `scripts/start-session.sh` to keep handover synced.
   - End-of-task push: `scripts/push-and-verify.sh` (push + verify sync).
   - Auto-push if safe: `scripts/auto-push-if-safe.sh` (installed via `scripts/install-hooks.sh`).

- Canonical references: `docs/canonical-layer-model.md`, `docs/repo-assignment.md`.

## Quick Rules (see Constitution for full detail)
- Governed lifecycle only: Objective Intake -> Spec Elicitation -> Objective Contract -> Inference (Gap Ledger) -> Planning (Task Plan -> `todo.md`) -> Controlled Prototyping -> Lock-In -> Execution (PDCA) -> Verification.
- Attention-bounded interaction: one bounded question per turn with rationale and visible state.
- No inference, planning, or execution before Spec Elicitation is complete.
- Vibe coding is prohibited; agents must refuse to execute without an approved spec.
- No execution before a visible Task Plan exists in `todo.md`.
- All intake goes through the Prompt Debugger before governance; no silent fixes.
- No cross-repo changes without explicit coordination; execution obeys, governance decides.

If `CONSTITUTION.md` exists, it prevails over this file.
