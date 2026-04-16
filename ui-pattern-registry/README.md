# CERES UI Pattern Registry
Part of the CERES (Coordinated Emergent Reasoning System). Umbrella repo: [CERES](https://github.com/holaymolay/ceres-coordinated-emergent-reasoning-system).
**Hub entry:** Load CERES via the umbrella `PROMPTLOADER.md` + `CONSTITUTION.md` (hub repo) and use hub todo templates/init script when bootstrapping; this component stays independent and is pulled via hub clone/run scripts.




Machine-readable registry of allowable UI patterns for LLM-driven front-end systems, governed by the CERES.

## Purpose
- Finite vocabulary of structural UI patterns so agents select allowed layouts instead of inventing them.
- Renderer-agnostic definitions with explicit roles, constraints, and composability rules.
- Non-goals: styling, components, prompts, or framework coupling.

## What's Inside
- Pattern schema at `schemas/pattern.schema.json`.
- Starter patterns in `patterns/layouts`, `patterns/compositions`, and `patterns/interactions`.
- Validation tooling in `scripts/validate-patterns.js` plus tests and CI workflow.
- Project docs in `docs/` covering purpose, pattern definition, usage model, and versioning.

## Starter Pattern Set
- Layouts: `layout_hero_stack`, `layout_split_pane`.
- Compositions: `composition_card_group`, `composition_form_cluster`.
- Interaction: `interaction_primary_cta_flow`.

## Usage
- Install dependencies with `npm install` (or `npm ci`).
- Validate registry definitions via `npm run validate`.
- Run tests via `npm test` (includes validation and fixtures).
- CI runs lint, validation, and tests on push/PR (`.github/workflows/ci.yml`).

## Governance
- Governed by the CERES (`AGENTS.md`) with Concept `ui-pattern-registry` and Spec `999bd713-5142-49b2-92d9-f22b1ceea0f4`.
- Stack profile: `docs/stacks/ui-pattern-registry.md`.
- README is generated from `README_SPEC.yaml`; edit the spec and regenerate rather than editing this file directly.

## Versioning
- Repository and package version `0.1.0`; tag releases as `v0.1.0`, `v0.1.1`, etc.
- Patterns carry their own `version` and `status`; schema version recorded as `schema_version` in each file.
## Observability (local)
- Use  to emit stage events via hub .
