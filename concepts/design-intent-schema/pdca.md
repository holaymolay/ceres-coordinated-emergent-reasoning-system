# Design Intent PDCA Loop

This loop governs updates to the Design Intent schema and intent objects so changes remain explicit, validated, and immutable.

## Plan
- Define the goal change or routing constraint that requires a new intent.
- Update or reference the governing spec: `specs/design-intent-schema-v1.md`.
- Identify the intent attributes that must change and plan the new intentVersion.

Artifacts:
- Proposed intent object (new intentVersion).
- Spec updates when schema rules change.

## Do
- Implement schema changes (if needed) and update the validator.
- Create the new Design Intent object; do not edit the previous one in place.

Artifacts:
- Updated schema or validator (if required).
- New intent artifact with bumped intentVersion.

## Check
- Validate the intent with `handlers/intent/validate.py` and tests.
- Confirm routing assumptions align with the intent attributes.

Artifacts:
- Validation output and test results.

## Act
- Record the change in the changelog and handover notes.
- Archive prior intent versions for audit.
- Adjust documentation if the intent contract changes.

Artifacts:
- Changelog entry.
- Updated documentation (if required).

## Observability Hooks
- Count of intent validation failures.
- Drift rate between intentVersion and schemaVersion.
- Routing decisions that depend on Design Intent attributes.
