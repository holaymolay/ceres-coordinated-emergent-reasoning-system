Spec Title: README Spec Engine v1
Spec ID: 3d59c02d-db7b-46fa-b2fe-da42d5d1a7c5
User Story: As a systems architect, I need a deterministic, spec-driven README generator and validator so README quality is explicit, auditable, and enforceable elsewhere.

Functional Requirements:
- Provide CLI modes: generate, validate, diff.
- Generate README.md from README_SPEC.yaml plus repo metadata with deterministic output.
- Validate README.md against README_SPEC.yaml and YAML-defined rules; output pass/fail + reasons.
- Produce a semantic diff between README.md and regenerated README.
- Support README_SPEC.yaml fields: project_name, one_sentence_value_prop, audience (include/exclude), problem_statement, solution_summary, outcomes, quick_start, repo_map, non_goals, constraints (max_length, banned_terms, tone_profile).
- Provide example specs (minimal, advanced) and core spec YAMLs for sections/rules/tone.

Non-functional Requirements:
- No LLM calls or network dependence.
- Deterministic transformation and validation.
- CLI-first and agent-friendly usage.
- No enforcement logic specific to a single repo.
- Operate purely on explicit specs and repo metadata.

Architecture Overview:
- Python CLI scripts in src/ for generate, validate, diff.
- Shared helper utilities for YAML parsing, rendering, validation, and metadata collection.
- YAML-driven rules in spec/sections.yaml, spec/rules.yaml, spec/tone.yaml.

Language & Framework Requirements:
- Python 3.11.

Testing Plan:
- Manual CLI smoke checks for generate/validate/diff.

Dependencies:
- PyYAML for YAML parsing.

Input/Output Schemas:
- Input: README_SPEC.yaml, README.md, repo metadata (filesystem).
- Output: README.md, validation report, semantic diff text.

Clarifications (optional):
- Q: None. A: Requirements are explicit in the user request.

Validation Criteria:
- Repository structure matches required layout.
- README.md includes explicit disclaimers and spec-driven sections.
- CLI scripts run deterministically on provided specs.

Security Constraints:
- No external calls or secret handling.
