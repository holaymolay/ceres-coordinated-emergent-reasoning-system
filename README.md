# CERES — Coordinated Emergent Reasoning System (Umbrella)

CERES is the umbrella project and governing architecture for this ecosystem. It replaces human-centered coordination and judgment with a governed, closed-loop, agentic process for solving complex problems. This repository is the coordination entrypoint for CERES; it is **not** a monorepo and does **not** execute tools or enforce rules—enforcement and runtime behavior live inside the individual component repositories, which operate under CERES.

## Component Repositories
- `governance-orchestrator`: Governance/orchestration for coding agents (CERES subcomponent).
- `readme-spec-engine`: Spec-driven README generator and validator for deterministic documentation (CERES subcomponent).
- `spec-compiler`: Compiler-style CLI that turns clarified intent into governed specification artifacts (CERES subcomponent).
- `ui-constitution`: Machine-readable visual constitution defining enforceable UI constraints (CERES subcomponent).
- `ui-pattern-registry`: Registry of approved UI patterns for renderer-agnostic, LLM-driven front ends (CERES subcomponent).

## Workspace Model
- Parent (this repo): CERES coordination map, docs, and lightweight scripts only.
- Children: independent tools with their own governance, tests, and release cycles, operating under CERES authority.
- Git ignores children by design; no child content is tracked here, and removal of this repo must not affect runtime behavior of any component.

## Prompt Debugger & Schemas
- Pre-governance gate: `prompt-debugger/cli.py` (outputs Prompt Debug Report).
- Schemas: `schemas/objective_contract.schema.json`, `schemas/gap_ledger.schema.json`, `schemas/task_plan.schema.json`, `schemas/completed_entry.schema.json`, `schemas/prompt_debug_report.schema.json`.
- All intake (task-inbox/chat) must pass the debugger before governance.

## Component management
- Components stay independent; this hub only references them.
- Clone missing components: `scripts/clone-components.sh` (reads repos.yaml; override org with `--org`).
- Run a command inside a component: `scripts/run-component.sh <component> "<cmd>"`.

## Todo artifacts
- Use `scripts/init-todo-files.sh [target-dir]` to copy CERES todo templates (`todo-inbox.md`, `todo.md`, `completed.md`, `handover.md`).
- Templates live in `templates/todo/`; keep formatting to satisfy governance gates.

## Component routing
- See `docs/routing.md` for which component to invoke and how to call it via hub scripts.

## Spec Elicitation Agent (SEA)
- Run SEA before Objective Contracts/Specs/Gap Ledgers/Planning.
- Instructions: `docs/sea.md`; artifact template: `templates/elicitation/elicitation.md`.
- SEA is read-only and stops after emitting `elicitation.md` (no planning or code).
