# Usage Model

The registry is consumed by LLM planning layers, renderer adapters, and CI so every generated UI references an approved pattern.

## How consumers use the registry
- **Planning / prompting**: LLMs select a `pattern_id` and variant instead of free-form layout invention.
- **Renderer adapters**: Map pattern roles/parts to framework-specific components while honoring `max_nesting_depth` and composability rules.
- **Validation**: CI and local tooling validate pattern files plus generated payloads against `schemas/pattern.schema.json`.

## Validation workflow
1. Install dependencies: `npm install` (or `npm ci`).
2. Run schema validation: `npm run validate` (uses `scripts/validate-patterns.js`).
3. Run tests: `npm test` (validates plus fixture checks).
4. CI (`.github/workflows/ci.yml`) runs lint → validate → tests on every push/PR; failures block merges.

## Integration guidelines
- Treat `pattern_id` as the contract key between LLM outputs and renderers.
- Honor `allowed_page_goals`, `allowed_interaction_density`, and `forbidden_intents` when selecting patterns.
- Enforce `composability` rules: only nest child categories/IDs that the pattern allows; reject incompatible combinations upstream.
- Keep renderer- or product-specific decisions outside this registry; adapters own styling and behavior.
