# Design Intent Schema (Concept)

## Purpose
Define a machine-readable Design Intent contract that explains why a frontend exists and what it must optimize for, without specifying rendering details.

## Boundaries
- Intent only; no UI components, styling, or renderer logic.
- Frontend-agnostic and reusable across projects.
- Routing and agent behavior may reference intent attributes, but rendering remains out of scope.

## Intent Lifecycle
### Creation
- Produce a Design Intent object before any UI intent or rendering work begins.
- Required metadata: schemaVersion, intentId, intentVersion, createdAt.
- Treat the intent as an API contract tied to the product goal.
- Keep brand_traits to five entries or fewer to preserve a crisp, enforceable intent.

### Validation
- Validate with the JSON Schema and `handlers/intent/validate.py` before use.
- Missing or invalid intent blocks downstream execution.

### Immutability
- Design Intent is immutable once created.
- Any change requires a new intent object with a bumped intentVersion and new createdAt timestamp.

### Versioning
- schemaVersion follows semantic versioning; breaking schema changes increment the major version.
- intentVersion increments on any change to intent content; prior versions remain archived for audit.

## Agent Consumption Rules
- Agents must treat Design Intent as mandatory input.
- Agents must not mutate intent in place; propose a new intent object instead.
- Routing decisions may depend on page_goal, audience_sophistication, interaction_density, and expressiveness_tolerance.

## Folder structure
- handlers/intent: validation logic.
- tests: fixtures and validation tests.

## Schema location
- `schemas/design-intent.schema.json`
