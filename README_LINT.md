# README lint rules
This document defines README linting rules and autofix guarantees.
It describes what the lint check enforces and how fixes behave.
Use it to understand the README governance boundary.
Autofix is conservative and does not rewrite content.

## Lint rules
- Title must be a single H1 at the top of README.md.
- Value proposition sentence must end within the first 10 lines.
- Required sections must appear in canonical order.
- Banned headings are disallowed in section titles.
- README length must stay within the configured line cap.
- Exclamation points are limited to prevent hype.

## Canonical section order
Sequence 1 covers the opening structure.

1. Title + One-Sentence Value Proposition
2. Who This Is For
3. Core Problem
4. Solution
5. Outcomes

Sequence 2 covers execution and constraints.

1. How It Works
2. Quick Start
3. Repository Map
4. Non-Goals / Design Philosophy

## Autofix guarantees
- Does not rewrite prose or add claims.
- Does not add or remove links.
- Adds missing section headers with TODO stubs.
- Normalizes headings to canonical names.
- Reorders sections to the canonical order.
- Trims excessive blank lines.

## Usage
- Check mode: `python scripts/readme_lint_autofix.py --check`
- Fix mode: `python scripts/readme_lint_autofix.py --fix`
