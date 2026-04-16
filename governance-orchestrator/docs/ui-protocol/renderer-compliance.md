# UIP Renderer Compliance Checklist

This checklist certifies that a renderer is UIP-compliant. Each item is pass/fail only.

## 1. Input guarantees
- [ ] Accepts only validated UIIntent objects.
- [ ] Rejects unknown `schemaVersion` values.
- [ ] Does not infer semantics beyond intent fields.

## 2. Output guarantees
- [ ] Emits UIEvent objects only.
- [ ] Includes required fields (`intentId`, `idempotencyKey`, `uiSessionId`, `schemaVersion`).

## 3. Behavior guarantees
- [ ] No domain state mutation.
- [ ] No business logic.
- [ ] No agent callbacks.
- [ ] No cross-intent inference.

## 4. Styling guarantees
- [ ] Uses tokens + patterns only.
- [ ] No ad-hoc or inline styling logic.

## 5. Determinism test
- [ ] Same input produces the same structural output and event class sequence.

## Certification test (simple)
1. Feed a fixed UIIntent fixture into the renderer twice.
2. Compare serialized structural output and emitted UIEvents.
3. Pass if outputs match exactly; fail otherwise.

## Pass/Fail criteria
- Pass only if all checklist items are satisfied.
- Fail if any item is unchecked or unverifiable.

## Certification workflow
Renderer certification is executed in CI via `scripts/check-renderer-certification.py` and described in `docs/ui-protocol/renderer-certification.md`.
