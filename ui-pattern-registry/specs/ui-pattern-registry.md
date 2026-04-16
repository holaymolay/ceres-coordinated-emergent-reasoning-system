Spec Title: UI Pattern Registry v0.1.0
Spec ID: 999bd713-5142-49b2-92d9-f22b1ceea0f4
User Story: As a design system governance owner, I need a machine-readable registry of allowable UI patterns with enforced validation so that LLM-driven front-end systems reuse consistent structures instead of inventing new ones.

Functional Requirements:
- Adopt the Context-Engineering Framework governance in this repo (AI-operated, spec-first, ledger/todo artifacts present) and align stack profile to the tooling used for the registry.
- Define a pattern schema (JSON Schema) capturing structural fields: pattern_id, category (layout|composition|interaction), description (structural only), required_roles, optional_variants, max_nesting_depth, usage constraints (allowed_page_goals, allowed_interaction_density, forbidden_intents, animation_allowed, composability rules), and metadata for validation/versioning.
- Provide an initial starter pattern set: at least two layout archetypes, two component compositions, and one interaction flow, all validating against the schema.
- Implement validation tooling that parses all patterns (YAML/JSON), validates against the schema, and fails CI on invalid or incomplete definitions.
- Add documentation explaining purpose, what counts as a pattern vs non-pattern, usage model for consumers/enforcers, and versioning approach for the registry.
- Produce an initial tagged release version v0.1.0 and align repository metadata to that version.

Non-functional Requirements:
- Patterns must remain structural (no styling tokens, renderer or framework coupling, no prompts/agent logic).
- Outputs must be deterministic and machine-readable; validation should be scriptable via CI.
- Keep dependencies minimal and security-conscious; no network calls in validation.
- Favor explicitness and clarity over coverage; avoid speculative abstractions.

Architecture Overview:
- Directory layout: `/schemas` for JSON schemas, `/patterns/<category>/` for YAML pattern definitions, `/docs` for project docs, `/scripts` for validation tooling, `/tests` for validation tests, `/ai_workflow_revisions` (gitignored) for workflow snapshots.
- Validation pipeline: Node.js-based script that loads schema, parses all pattern files, enforces schema, and returns non-zero on validation errors; GitHub Actions CI runs lint + validation + tests.
- Stack alignment: npm project configured for Node 20 with ESLint and Node test runner for validation tests.

Language & Framework Requirements:
- Node.js 20 LTS, npm as package manager.
- JavaScript (ESM) for validation tooling and tests; use `ajv` (or similar) for JSON Schema validation and `yaml` parser for YAML files.
- ESLint with recommended settings for scripts/tests.

Testing Plan:
- `npm run lint` for static analysis of scripts and tests.
- `npm run validate` to run schema validation across all pattern files.
- `npm test` to run validation plus unit tests (Node test runner) covering success/failure cases.
- GitHub Actions workflow to run lint/validate/tests on push and PR; CI must fail on schema violations.

Dependencies:
- npm dependencies: `ajv` (with formats if needed), `yaml`, `glob`.
- Dev dependencies: ESLint + Node typings if needed.
- No runtime external services.

Input/Output Schemas:
- Pattern schema defines required fields listed above plus metadata (name/title, version, status) with enum constraints where applicable.
- Pattern files are YAML adhering to the schema; validation script outputs human-readable errors per file and a non-zero exit code on failures.

Clarifications (optional):
- None at this time.

Validation Criteria:
- All pattern files validate against the schema without warnings/errors.
- CI workflow fails on any invalid schema violations or lint/test failures.
- Documentation covers purpose, scope, usage model, non-goals, and versioning.
- Repository version/tag set to v0.1.0 and reflected in package metadata/docs.

Security Constraints:
- No secrets or external network calls required for validation.
- Keep dependencies pinned in `package-lock.json`; run npm audit as part of hygiene when applicable.
- Avoid storing generated artifacts or credentials in the repo.
