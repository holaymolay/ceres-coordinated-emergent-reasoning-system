# Golden Path Integration Test

This directory contains a self-contained, minimal witness that the spec compiler can ingest a valid design intent and renderer manifest, pass them through the same validation entrypoints real users run, and produce deterministic pass/fail outcomes.

What it proves:
- A valid design intent is accepted.
- A valid renderer output passes renderer-contract and taste enforcement.
- A single, intentional violation fails with a precise, attributable message.

Why it exists:
- To guard against regressions that would silently break the happy path across contract validation and taste enforcement.
- To keep the proof isolated from production logic so runtime behavior is unchanged if this directory is removed.

Notes:
- Fixtures live only here; production code never imports from this path.
- The test uses the shipped ruleset, renderer contract schemas, and stage runners (`renderer-validate` and `taste`) rather than mocks or shortcuts.
