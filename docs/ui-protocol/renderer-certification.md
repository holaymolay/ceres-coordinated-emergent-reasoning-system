# UIP Renderer Certification

This document defines the CI certification checks for UIP renderers. The checks are deterministic and fail the build on non-compliance.

## Scope
- Each renderer is declared in `ui-contracts/renderers.yaml`.
- CI runs `scripts/check-renderer-certification.py` to certify each renderer entrypoint and adapter.

## Pass/Fail Rules
### Input tests (blocking)
- Valid UIIntent fixture passes validation.
- Invalid UIIntent fixture is rejected (must include schemaVersion failure).
- Renderer entrypoint calls `assertValidUiIntent` or `validateUiIntent`.

### Output tests (blocking)
- Renderer event fixture is a JSON object.
- Event fixture includes `intentId`, `uiSessionId`, `idempotencyKey`, and `schemaVersion`.

### Behavior tests (blocking)
- Renderer entrypoint and adapter do not import Concepts, agents, or skills.
- Renderer code avoids nondeterministic calls (`Math.random`, `Date.now`, `crypto.randomUUID`).

### Styling tests (blocking)
- Adapter uses tokenized styling (requires `tailwindTokens` import).
- Adapter avoids inline className strings (`className="..."` or `className='...'`).

## Certification outcome
- Fail on any unmet rule.
- Pass only when all checks succeed.
