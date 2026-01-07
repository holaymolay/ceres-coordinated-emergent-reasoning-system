# Prompt: Recursive execution planning step

Prompt ID: f9635103-b61e-4beb-aea0-20a1b4ea3356
Classification: atomic
Status: draft
Owner: user
Created: 2026-01-07T18:12:19.933566Z
Last-Modified: 2026-01-07T18:12:19.933566Z

## Intent
Define non-authoritative planner signaling for execution pressure.

## Constraints
- Add a single todo item only.
- No execution or implementation.
- Do not add extra steps.

## Task Decomposition Guidance (decomposable only)
N/A

## Prompt Body
Add exactly one todo item to define non-authoritative execution-pressure signals that planners or agents may emit.

The todo must:
- explicitly state that signals do NOT change execution
- define when signals may be emitted
- define when they must NOT be emitted
- prohibit signals from carrying authority or intent

Constraints:
- Planning only; do not implement.
- One todo item only.
- Use imperative voice, atomic, testable, with a short parenthetical intent note.


## Validation Criteria
- Exactly one todo item added.
- Todo is imperative, atomic, testable, and includes a short parenthetical intent note.
