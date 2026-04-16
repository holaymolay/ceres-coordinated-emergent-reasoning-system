Spec Title: Design Intent Schema v1
Spec ID: 193e018f-6875-4276-b503-2af48f6ec37b
Skill: none (no applicable Skill)
User Story: As a delivery team, I need a deterministic Design Intent Schema so agents can reason about why a frontend exists and what it must optimize for without specifying rendering details.

Functional Requirements:
- Define a Design Intent Schema with required fields: page_goal, audience_sophistication, brand_traits (max 5 entries), interaction_density, expressiveness_tolerance, accessibility_floor.
- Encode lifecycle semantics: intent creation metadata, validation requirements, immutability rules, and versioning strategy.
- Integrate into agent orchestration: agents must consume Design Intent as input; agents must not mutate intent; routing may depend on intent attributes.
- Validation must fail fast on invalid or missing intent and block downstream execution.
- Provide minimal tests that confirm valid intent passes and invalid intent fails.

Non-functional Requirements:
- Deterministic, enforceable, reusable across projects, frontend-agnostic.
- No UI rendering rules, visual tokens, components, or aesthetic decisions.

Architecture Overview:
- Concept: `concepts/design-intent-schema/` owns intent governance artifacts.
- Schema: `schemas/design-intent.schema.json` (JSON Schema draft 2020-12).
- Validator: `concepts/design-intent-schema/handlers/intent/validate.py`.
- Tests + fixtures: `concepts/design-intent-schema/tests/`.

Language & Framework Requirements:
- Python 3.11 for validation logic/tests.
- JSON Schema (draft 2020-12) for the intent contract.

Testing Plan:
- Run `python3 concepts/design-intent-schema/tests/test_validation.py`.

Dependencies:
- None.

Input/Output Schemas:
- Design Intent JSON Schema: `schemas/design-intent.schema.json`.

Clarifications (optional):
- None.

Validation Criteria:
- Schema enumerations match the required intent fields and enforce brand_traits max length (5 entries).
- Validator fails fast on missing or invalid intent and rejects extra fields.
- Tests prove valid intents pass and invalid intents fail.
- Documentation explains what Design Intent is, why it exists, how agents consume it, and how versioning/immutability work.

Security Constraints:
- No network access or secret handling.
