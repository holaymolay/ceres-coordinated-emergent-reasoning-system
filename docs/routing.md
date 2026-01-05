# CERES Component Routing (Reference)

Use this map to decide which component to invoke. Components remain independent; pull/execute via hub scripts (`scripts/clone-components.sh`, `scripts/run-component.sh`).

- governance-orchestrator: lifecycle gates, arbitration, planning enforcement, gap handling, attention-bounded questioning. Run governance checks here.
- readme-spec-engine: deterministic README generation/validation from README_SPEC.yaml. Do not free-write READMEs.
- spec-compiler: intent/spec compilation pipeline; produces governed specification artifacts.
- ui-constitution: machine-readable UI constraints; authoritative UI rules.
- ui-pattern-registry: approved UI patterns/registry for renderers.
- parallel-agent-runner: optional parallel command runner for agent CLIs.

Umbrella helpers:
- Component management: `scripts/clone-components.sh` (clone missing), `scripts/run-component.sh <component> "<cmd>"` (invoke inside component).
- Todo templates/init: `scripts/init-todo-files.sh` (todo-inbox, todo, completed, handover).
- Prompt Debugger: `prompt-debugger/cli.py` (required pre-governance gate); schemas live in `schemas/`.

Bootstrap entry for new projects: use `PROMPTLOADER.md` + `CONSTITUTION.md` from the hub. Clone components only as needed.
