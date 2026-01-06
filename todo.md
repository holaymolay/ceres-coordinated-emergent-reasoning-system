# Todo (CERES template)

## Bugs
- [ ]

## Workflow Governance
- [x] Enforce SEA integration: document invocation in PROMPTLOADER/README and ensure governance references SEA phase ordering.

## Current Focus
- [x] Implement inference enforcement: Gap Ledger stage with interrogator/resolver policies in governance runtime.
- [x] Wire observability hooks across components using `scripts/log_event.py` (stage transitions, gate outcomes).
- [x] Produce canonical layer/repo diagram and fill dev_notes/0 A canonical_layer_model.md.
- [x] Align spec-compiler/readme-spec-engine to consume hub schemas (Objective Contract, Gap Ledger, Task Plan, Prompt Debug Report).

## Prompt Execution (Sequential)
Execute these in order; do not start prompt_N+1 until prompt_N is complete.
- [x] Execute `dev_notes/prompt_1_enforcement layer.md`.
- [x] Execute `dev_notes/prompt_2_concept_dependency_graph.md`.
- [x] Execute `dev_notes/prompt_3_splitting_ceres_core_and_workspace.md`.
- [x] Execute `dev_notes/prompt_4_deterministic_arbitration_rules.md`.
- [x] Execute `dev_notes/prompt_5_planner_output_standardization.md`.
- [ ] Execute `dev_notes/prompt_6_adding_additional_skills.md`.
- [ ] Execute `dev_notes/prompt_7_improving_the_ui_layer.md`.
- [ ] Execute `dev_notes/prompt_8_modular_plugin_architecture.md`.
- [ ] Execute `dev_notes/prompt_9_python_fallback_scripts.md`.
- [ ] Execute `dev_notes/prompt_10_formal_parity_verification_checklist.md`.

## Next Features & Updates
- [x] Add strict todo template hash/header validation to lifecycle gate.
- [x] Extract observability into dedicated repo once hooks are in place.

## Backlog
- [x] Add advisory Concept/Synchronization signal capture post-elicitation (non-binding) helper script.