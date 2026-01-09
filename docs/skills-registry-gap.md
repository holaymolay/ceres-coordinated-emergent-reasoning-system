# Skills Registry Gap Memo

## Summary
CERES already has governed agent skills for execution control; Obsidian Skills is a human-facing knowledge model. The missing layer is a human-readable registry/projection of existing CERES skills.

## Decision
Add a read-only skills registry projection that mirrors governance-defined skills without redefining them.

## Rationale
- Keeps governance as the single source of truth.
- Improves human discoverability without changing enforcement behavior.

## Scope Notes
- No new skills are introduced in this step.
- No enforcement or schema changes are required to publish the projection.
