# UI Intent PDCA Loop

This loop governs UI refinement without direct JSX, HTML, or Tailwind edits. All changes flow through the intent schema, adapter token maps, and layout pattern selection.

## Plan
- Define the proposed change (schema evolution, token adjustment, or layout pattern selection).
- Update or reference the governing spec: `specs/ui-intent-protocol-v1.md`.
- Identify affected intents, patterns, and tokens.

Artifacts:
- Spec updates (if schema or rules change).
- Proposed intent sample(s).
- Pattern selection notes (if layout changes).

## Do
- Implement the schema/type update or adapter token/pattern change.
- Keep JSX confined to the adapter layer; do not edit JSX directly for a visual change.

Artifacts:
- Updated `concepts/ui-intent-protocol/handlers/intent/intent.schema.json` or intent types.
- Updated `concepts/ui-intent-protocol/handlers/adapter/tokens.ts` or `patterns.ts`.
- Updated Skill validation rules if schema changes.

## Check
- Validate intents against the schema (via `ui_intent.emit` or other validators).
- Verify adapter resolution (intent -> pattern -> components) against reference intent(s).
- Record failures and drift (missing fields, unsupported pattern IDs, token gaps).

Artifacts:
- Validation output (skill run results or test output).
- Adapter mapping review notes.
- Issue list with root cause tags (schema, tokens, patterns).

## Act
- Refine schema version, token maps, or pattern resolver logic based on Check findings.
- Record the decision and update the spec or design-decision wiki entry if architectural.

Artifacts:
- Updated schema version (when breaking changes occur).
- Changelog entry and handover notes.

## Observability Hooks
- Count of validation failures by intent type.
- Distribution of resolved layout patterns.
- Token usage coverage (tokens referenced vs. defined).
- PDCA cycle duration and first-pass success rate.

## Example Refinement Cycle
Plan:
- Need: form intents should prioritize a single-column layout for clarity.
- Proposed change: enforce "single-column" for form.create in the pattern resolver.

Do:
- Update `patterns.ts` to map form.create to single-column.

Check:
- Run the reference form intent through the adapter; confirm the pattern resolves correctly.

Act:
- Record the pattern mapping decision in the spec or design decisions log.
