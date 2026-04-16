# README quality rubric
This rubric defines the required README narrative standard.
It is the authoritative baseline for README quality enforcement.
Use it to review changes before merging.
CI checks must align with these requirements.

## Purpose clarity
- The README answers what this is in one sentence.
- The sentence describes governance and context engineering.

Fail if:
- A reader cannot explain the purpose after 10 seconds.

## Audience fit
- The README states who should use it.
- The README excludes at least one non-target audience.

Fail if:
- The reader must infer applicability.

## Problem framing
- The README names agent failure modes:
  - ambiguity
  - clarification loops
  - non-determinism
  - lack of auditability

Fail if:
- The problem is framed as better prompts or better models.

## Solution framing
- The README explains the solution in structural terms:
  - specs
  - skills
  - enforcement
  - artifacts
  - governance

Fail if:
- The solution relies on vibes or heuristics.

## Outcomes over features
- The README lists concrete outcomes.
- Outcomes are measurable or falsifiable.

Fail if:
- Feature lists dominate without outcomes.

## Execution path
- The README includes a Quick Start.
- The entry path is obvious without extra documents.

Fail if:
- A reader cannot see how to begin using the framework.

## Non-goals explicitness
- The README states what the framework does not solve.

Fail if:
- The scope appears unlimited or ambiguous.

## Tone and discipline
- The README is technical, neutral, and direct.
- No hype, emojis, or motivational language.

Fail if:
- Marketing language appears.

## Structural integrity
- The flow is problem to solution to outcomes to usage.
- Sections are distinct and not interchangeable.

Fail if:
- Sections are duplicated or vague.

## Merge standard
- CI passes.
- All rubric sections are satisfied.
- No narrative regression is introduced.

## Why this matters
The README is a governance artifact, not documentation fluff.
It shapes how humans and agents reason about the system.
