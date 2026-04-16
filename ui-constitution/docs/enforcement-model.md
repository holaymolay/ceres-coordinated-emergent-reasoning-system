# Enforcement Model

## Validation Target
The Visual Constitution is validated as a JSON object against `constitution/constitution.schema.json`.
Each domain schema defines hard limits; missing or extra fields are violations.

## Violation Semantics
- Any JSON Schema validation error is a violation.
- A constitution document is compliant only if it passes full validation with zero errors.
- A UI system is compliant only if its outputs are restricted to values defined by the constitution (for example, font sizes, spacing values, role-based colors, motion durations).

## Color Contrast Enforcement
Contrast constraints are defined by role pairs and minimum ratios.
A theme or renderer must compute contrast ratios for each required pair and fail compliance when any ratio is below the declared minimum.

## No Defaults
The constitution does not imply defaults or preferences. All required fields must be present with explicit values.
