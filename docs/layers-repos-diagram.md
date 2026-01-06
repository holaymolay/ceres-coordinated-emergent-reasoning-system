# CERES Layer ↔ Repo Map (Text Diagram)

Canonical references: `docs/canonical-layer-model.md`, `docs/repo-assignment.md`.
Conceptual repos (not yet extracted): Execution runtime, Observability, Security & Access, Spec Library.

Layers (from canonical model) and current repo authority:

- Interface / Intake / Elicitation / Inference / Planning / Governance (0-5):
  - governance-orchestrator (enforces gates, planning, arbitration; uses hub Prompt Debugger + schemas)
  - hub (CERES umbrella) for PROMPTLOADER, Constitution, schemas, prompt-debugger, todo templates
- Execution (6):
  - runtime agents (model-specific; obey governance outputs)
- Verification (7):
  - runs/tests in each component as needed; governance enforces before completion
- Observability (8):
  - hub `scripts/log_event.py` helper; to be wired across components; extraction planned later
- Persistence/Memory (9):
  - memory ledger (`memory.md`), run receipts (`runs/`), `completed.md`, Gap Ledger; `handover.md` as export snapshot; hub standards apply
- Feedback/PDCA (10):
  - completed entries and governance updates; closed-loop adjustments

Component roles:
- governance-orchestrator: lifecycle gates, gap enforcement, planning/arbitration
- spec-compiler: intent/spec compilation; should consume hub schemas
- readme-spec-engine: README generation/validation; spec-driven
- ui-constitution: UI constraints
- ui-pattern-registry: UI patterns
- parallel-agent-runner: optional parallel execution helper

Use hub scripts to clone/invoke components (independent repos): `scripts/clone-components.sh`, `scripts/run-component.sh <component> "<cmd>"`.
