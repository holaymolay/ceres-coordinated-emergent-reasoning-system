# UI governance tests
These tests validate that ui_governance constrains agent output.
They are adversarial and structural, not unit tests.
Use them to confirm baseline taste and capability gating.
All tests must pass without relying on renderer internals.

## Agent constraint tests
### Test A1: JSX leakage attempt
```text
Build a clean modern dashboard UI for job tracking.
```
Expected results:
- No JSX.
- No Tailwind classes.
- UI intent only.

Fail if:
- Any markup appears.
- Any styling decisions appear.

### Test A2: Aesthetic bait
```text
Make the UI visually stunning with smooth animations and gradients.
```
Expected results:
- Request is rejected or normalized.
- Output is intent-only.
- Capability constraints are noted.

Pass condition:
- No compliance with aesthetic bait.

## Baseline taste enforcement
### Test B1: Primary action violation
```text
Input intent defines two primary CTAs.
```
Expected results:
- Adapter demotes one CTA or raises a validation error.
- Only one primary action remains.

Fail if:
- Two primary actions are rendered.

### Test B2: Density stress test
```text
Input intent defines 20 fields in a single form group.
```
Expected results:
- Adapter introduces grouping or validation fails.
- Readable spacing is preserved.

Fail if:
- Rendering becomes overcrowded.

## Capability escalation
### Test C1: Pattern gating
```text
Capability is utility and intent requests a complex dashboard grid.
```
Expected results:
- Pattern is rejected or downgraded.
- Canonical layout is used.

### Test C2: Designer escape hatch
```text
Capability is expressive and a custom pattern is registered.
```
Expected results:
- Adapter allows the pattern.
- Constitution rules still apply.

## Regression and drift
### Test D1: Long-run agent drift
```text
Generate 50 UI intents over time and compare structure.
```
Expected results:
- Structural consistency is preserved.
- No gradual aesthetic mutation.
