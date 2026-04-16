# Strict-ci profile
Use this profile for the most critical documentation surfaces.
It enforces the full Structured Richness rules with stricter language checks.
Choose it for public-facing docs and long-lived references.
This profile treats warnings as errors in automated checks.

## When to use
This profile is intended for high-visibility documentation.

- Core documentation sets.
- Public-facing guides.
- Long-lived reference material.

## What it enforces
It enforces all baseline rules with strict language validation.

- One H1 and sentence-case headings.
- H3 maximum heading depth.
- Markdownlint failures are fatal.
- Vale warnings treated as errors.
- No ambiguous language.

## What it relaxes
No relaxations beyond the base spec.

- None.

## Why it exists
Strict-ci protects critical docs from drift and ambiguity.
It keeps public documentation predictable and low risk to maintain.
