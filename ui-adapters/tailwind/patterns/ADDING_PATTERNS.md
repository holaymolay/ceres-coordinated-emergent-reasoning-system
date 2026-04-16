# Adding Tailwind Patterns

## Determinism Rules
- Match and rank functions must be pure and deterministic.
- Do not access time, randomness, or external state.

## Token-Only Tailwind Usage
- All Tailwind classes must come from the provided token set.
- Do not inline classes outside pattern renderers.

## Match + Rank Guidance
- `match(intent)` should be narrow and explicit for the intent type.
- `rank(intent)` should reflect priority within the matching group.
- Ties are resolved by patternId sorting, so keep IDs stable.

## Required Tests
- Add a selector test to confirm the pattern can be selected.
- Add or update registry tests to include the new pattern.
