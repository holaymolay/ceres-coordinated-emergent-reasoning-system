# UI Intent Emit Skill (Shared Package)

## Purpose
Produce validated UI intent objects deterministically from structured inputs. This skill forbids JSX, HTML, CSS, Tailwind classes, or any rendering output.

## Determinism
- Pure input -> output; no network calls.
- No filesystem writes.
- No runtime randomness or timestamps.

## Schema Compatibility
- Compatible with UI intent schema version: 1.0.0

## Integration Note
A host agent/tool calls the skill with a JSON payload containing a candidate UI intent object, validates it against the schema, and consumes the emitted intent artifact. Rendering remains the adapter's responsibility.

## Files
- `src/types.ts`: UI intent type definitions (mirror of the shared schema).
- `src/schema.ts`: schema validators (zod).
- `src/emit.ts`: deterministic emit helpers.
- `examples/`: sample intent payloads.
- `tests/emit.test.ts`: schema validation tests.
