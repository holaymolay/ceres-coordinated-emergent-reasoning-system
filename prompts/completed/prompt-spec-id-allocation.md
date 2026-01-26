# Prompt: Spec-ID allocation

Prompt ID: 4778b869-93b6-44e4-bbb2-ad2948dbc85a
Status: draft
Classification: atomic
Owner: user
Created: 2026-01-07T07:32:13.978015Z
Last-Modified: 2026-01-07T07:32:13.978015Z

## Intent
Define the minimal, authoritative spec-id allocation point and the smallest reversible change set to implement it.

## Constraints
- Governance-compatible change only.
- Keep scope minimal and reversible.
- No unrelated refactors.

## Prompt Body
1. Intent
   Identify the minimal spec-id allocation point that occurs before planning begins.
2. Constraints
   Keep the change set small, reversible, and governance-aligned.
3. Scope
   Focus on spec-id allocation at end of elicitation and propagation to required artifacts.
4. Inputs
   Use the following authoritative input as source text:

Excellent. You now have a closed, auditable control loop with a clean working tree. This is the right moment to choose the next capability upgrade deliberately, not reflexively.

Here is the honest recommendation:

Choose Spec-ID Allocation next (Pattern classification comes after, and will benefit from this.)

Why spec-ID comes first
Right now:
- Failure events are correct and truthful
- But early-stage failures cannot be correlated across:
  - retries
  - agents
  - downstream artifacts
- Pattern classification assumes you can trace behavior across time

A stable, early Spec ID gives you:
- Correlation across all gate events
- Deterministic replay
- Clean audit trails
- A hard anchor for pattern usage analysis later

Without it, pattern classification will be theoretical instead of measurable.

What “Spec-ID Allocation” actually means (tight scope)
This is not a big feature.

Minimal goal
Introduce a single, authoritative point where a real spec_id is minted before planning begins.

Where it should happen
At the end of elicitation, when:
- ready_for_planning: true
- blocking_unknowns: []

What changes
1. Allocate a real spec_id (UUID or hash)
2. Persist it into:
   - elicitation.md (front matter)
   - objective-contract.json
3. Emit a gate:pass event:
   - type: spec_allocated
   - context includes spec_id

From that point on:
- All failures include spec_id
- All observability becomes correlatable

Why not pattern classification yet
Pattern classification is policy.
Spec-ID allocation is infrastructure.
You always lay infrastructure first.

Next step (if you agree)
Proceed with spec-ID allocation, and draft:
- the exact allocation rule
- where the code lives
- the observability event
- a Codex-ready prompt
- a small and reversible change set

5. Required Reasoning
   Explain why spec-id allocation precedes pattern classification and define the smallest viable implementation.
6. Output Artifacts
   Produce a brief implementation plan and exact change locations (files and phases).
7. Validation Criteria
   The output must define where the spec_id is minted, where it is persisted, and the required observability event.
