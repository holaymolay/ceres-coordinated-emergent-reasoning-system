# Skill Package Template

Use this template to add a new deterministic Skill under `skills/<skill-slug>/`.

## Metadata
- Skill ID: `<id>` (dot namespace, snake segments; example: `schema.validate_json`)
- Skill Slug: `<skill-slug>` (kebab-case; example: `schema-validate-json`)
- Governing Spec ID: `<SPEC-...>` (required)
- Concepts: `<optional list>` (empty for shared infra)
- Synchronizations: `<optional list>` (required if cross-concept side effects exist)

## Scope (what this Skill does)
- One sentence, deterministic outcome, no business logic.

## Contract
- `skill.yaml` must conform to `skills/_schema/skill.schema.json`.
- Inputs: `schemas/input.schema.json` (JSON Schema; stdin JSON)
- Outputs: `schemas/output.schema.json` (JSON Schema; stdout JSON)

## Determinism Requirements
- No LLM calls; no prompts inside implementations.
- No network I/O unless explicitly declared and Security-approved.
- No wall-clock time reads unless constrained to `determinism.time: input_only`.
- No randomness unless seeded via input (`determinism.randomness: seeded`).

## Security / Access Declarations
- Declare all filesystem/env/subprocess/network access in `skill.yaml:security.access`.
- Do not add secrets to the repo. Use documented env keys and secure secret managers.

## Implementation
- Put executable entrypoints under `impl/`.
- Use `runtime.command` to call the entrypoint with relative paths only.
- Keep implementation stateless (no persistence outside declared filesystem write globs).

## Tests & Fixtures
- Add offline tests under `tests/` and deterministic fixtures under `fixtures/`.
- Tests must run without network access and without relying on wall-clock time.

## Validation Checklist
- [ ] `skill.yaml` validates against `skills/_schema/skill.schema.json`
- [ ] Input/output schemas are present and validate fixtures
- [ ] Implementation is deterministic and stateless
- [ ] Tests pass offline
- [ ] Spec ID is present and correct
