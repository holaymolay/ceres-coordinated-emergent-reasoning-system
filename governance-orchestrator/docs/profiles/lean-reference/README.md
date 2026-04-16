# Lean-reference profile
Use this profile for reference material that favors density over prose.
It keeps structure checks but relaxes language rules for minimal friction.
Choose it for specs, schemas, and machine-adjacent docs.
This profile skips callouts and heavy style enforcement.

## When to use
This profile is intended for structured reference content.

- API docs.
- Specs and protocols.
- Schemas and contracts.
- Generated or machine-adjacent docs.

## What it enforces
It enforces structural rules without narrative constraints.

- One H1 and ordered heading levels.
- H3 maximum heading depth.
- No raw HTML.
- Markdownlint rules enforced.

## What it relaxes
It relaxes rules that slow down reference writing.

- No callouts allowed.
- Vale checks disabled.
- Longer paragraphs allowed.

## Why it exists
Lean-reference preserves structure while minimizing authoring overhead.
It keeps reference docs consistent without forcing prose style rules.
