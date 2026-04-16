# UIP Enforcement

This document describes UIP-0.1 enforcement hooks and how to extend them.

## What is enforced
- Blunt output scan for JSX/HTML/Tailwind markers outside approved adapter/renderer allowlists (high false positives tolerated).
- Schema-aware artifact discovery + validation for UIIntent/UIEvent JSON (required fields + schemaVersion checks).
- Dependency direction checks (agents/skills cannot import adapters/renderers; renderers cannot import concepts/agents/skills; skills cannot import React/Tailwind).
- Event → Synchronization validation (UIEvent types must map to Synchronization triggers).
- Renderer certification checks (inputs, outputs, behavior, determinism) via CI.
- UIP-0.2 shadow validation (non-blocking, report-only).

## How enforcement runs
- CI runs `scripts/check-uip-compliance.sh`.
- The script fails fast with categorized UIP rule violations.
- Additional blocking checks run in CI for synchronization validation and renderer certification.
- UIP-0.2 shadow validation always reports and does not fail CI.
- Event synchronization validation: `scripts/check-uip-event-syncs.py`.
- Renderer certification: `scripts/check-renderer-certification.py`.
- UIP-0.2 shadow validation: `scripts/check-uip-shadow.py`.

## Blunt vs schema-aware checks
- Blunt scan: fast grep-based detection of UI markup/styling leakage outside adapter/renderer paths.
- Schema-aware gate: discovers UIP artifacts via `scripts/discover-uip-artifacts.py` and validates them with `scripts/check-uip-schemas.py`.

## Why false positives are acceptable
The forbidden-output scan is intentionally blunt to prevent UI leakage into agents, skills, and concepts. False positives should be resolved by relocating UI code into adapter or renderer allowlists.

## Adding new schemas safely
- Update schema constants (`skills/ui-intent-emit/impl/run.py`, `ui-contracts/events.schema.ts`) and any referenced JSON schema files.
- Add/update fixtures under `skills/ui-intent-emit/examples/` and `ui-contracts/examples/`.
- Update `scripts/check-uip-schemas.py` to allow the new schemaVersion(s) and required fields.
- If new artifact locations are introduced, register them in `scripts/discover-uip-artifacts.py`.

## Suppressing checks (explicit allowlist only)
- Blunt scan/boundary checks: extend the allowlist globs in `scripts/check-uip-compliance.sh` (see `SCAN_EXCLUDES` and `BOUNDARY_EXCLUDES`).
- Schema-aware validation: add repo-relative paths to `ALLOWLIST_PATHS` in `scripts/check-uip-schemas.py`.
- Do not suppress checks anywhere else.

## Extending enforcement
- Add new UIP checks to `scripts/check-uip-compliance.sh`.
- Add new UIIntent/UIEvent fixtures under `concepts/ui-intent-protocol/handlers/reference/` or `ui-contracts/examples/`.
- Keep failure messages actionable and deterministic.
