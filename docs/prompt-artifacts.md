# Prompt Artifacts (Long-Form Prompts)

This document defines how long-form prompts are stored, referenced, and executed in CERES.

## Purpose
- Keep `todo.md` legible by externalizing long prompts.
- Treat prompts as auditable, versioned inputs.
- Preserve governance and PDCA discipline without embedding large prompt bodies inline.

## Location and Naming
- Store long-form prompts in `prompts/` as `prompt-<slug>.md`.
- One prompt per file.
- `prompts/plan.md` and `prompts/execute.md` remain the canonical system prompts.

## Required Prompt File Structure

Each prompt file must follow this structure:

```md
# Prompt: <Short Name>

Prompt ID: <UUID or hash>
Status: draft | approved | deprecated
Classification: atomic | decomposable
Owner: <user|agent>
Created: <ISO-8601>
Last-Modified: <ISO-8601>

## Intent
One-paragraph description of what executing this prompt is meant to accomplish.

## Constraints
- Explicit constraints (scope, agents allowed, repos touched)
- Governance or security notes if relevant

## Prompt Body
<the full long-form prompt>
```

## Todo Integration Rule

`todo.md` must reference prompt files rather than embed long prompts.

Example (single task):

```md
- [ ] Execute prompt: prompts/prompt-spec-elicitation-auth.md
      Outcome: Produce complete Spec Elicitation artifact set
```

Example (decomposed tasks):

```md
- [ ] From prompt prompts/prompt-ui-constitution.md: Extract UI principles
- [ ] From prompt prompts/prompt-ui-constitution.md: Draft constitution schema
- [ ] From prompt prompts/prompt-ui-constitution.md: Validate against governance rules
```

Rules:
- One todo entry refers to one prompt file.
- Todo entries express intent and outcomes, not prompt text.
- Prompt files are the execution authority.

## Immutability and Revisions
- Prompt artifacts are read-only during execution.
- Modifying a prompt requires a new commit and updated metadata (`Last-Modified`, `Status`, and `Classification` if changed).
- Prompt ID may be rotated when materially revising content.

## Classification Gate (Mandatory)

Before planning tasks, the prompt must be classified as one of:

### Decomposable
A prompt is decomposable if it requests multiple separable outcomes, spans multiple concepts/phases, or allows meaningful partial completion.

Behavior:
- Store the prompt once.
- Create multiple `todo.md` entries that reference the same prompt.
- Each task must be independently testable and ordered when required.

### Atomic
A prompt is atomic if it produces one integrated outcome and splitting it would introduce ambiguity or loss of intent.

Behavior:
- Store the prompt once.
- Create a single `todo.md` entry referencing the prompt.
- The prompt body must use the 7-part structure:
  1. Intent
  2. Constraints
  3. Scope
  4. Inputs
  5. Required Reasoning
  6. Output Artifacts
  7. Validation Criteria

## Security Review

Prompts that touch authentication, secrets, or external systems must be reviewed by Security before execution.

## Lifecycle Alignment (PDCA)

- Plan: prompt created and referenced from `todo.md`.
- Do: prompt executed as a unit (atomic) or as decomposed tasks.
- Check: outputs validated against stated constraints.
- Act: prompt revised or deprecated as needed.
