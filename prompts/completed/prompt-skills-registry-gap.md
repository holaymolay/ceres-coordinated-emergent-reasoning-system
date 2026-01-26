# Prompt: Skills registry gap analysis

Prompt ID: 7082696a-c707-4fcc-9697-d04f4ca1fd2f
Status: draft
Classification: atomic
Owner: user
Created: 2026-01-07T07:29:37.441096Z
Last-Modified: 2026-01-07T07:29:37.441096Z

## Intent
Capture the current state of CERES skills versus Obsidian Skills and decide whether to add a human-facing skills registry or a projection of governance skills.

## Constraints
- Governance-compatible, doc-only analysis.
- Do not change enforcement or schemas.
- Do not add new skills; describe current state and optional next steps only.

## Prompt Body
1. Intent
   Confirm that CERES already has governed agent skills, contrast with Obsidian Skills, and decide whether to add a human-facing registry or projection.
2. Constraints
   Preserve governance rules; do not propose code changes in this pass.
3. Scope
   Focus on skills in governance and the optional human-facing layer only.
4. Inputs
   Use the following authoritative input as source text:

Below is a governance-compatible design that adds this capability to CERES without weakening any existing rules.

---

Feature: Externalized Long-Form Prompt Artifacts

Problem Addressed

Some prompts are:
- too long for `todo.md`
- semantically atomic (must not be split)
- operationally important (should be versioned, auditable, and executable)

Storing them inline in `todo.md` violates legibility and review discipline.

---

Solution Overview

Introduce a first-class Prompt Artifact mechanism:
- Long prompts live as standalone markdown files
- `todo.md` contains only a reference and execution intent
- Prompts are treated as immutable inputs to execution unless explicitly revised

This preserves:
- auditability
- PDCA discipline
- non-vibe-coding guarantees

---

Repository Additions

1. New Folder

/prompts/

Purpose:
- Store long-form, execution-bound prompts
- One prompt per file
- Markdown only

Naming convention:

prompts/
  prompt-<slug>.md

Example:

prompts/
  prompt-spec-elicitation-auth.md
  prompt-ui-constitution-pass.md

---

2. Prompt File Structure (Required)

Each prompt file must follow this structure:

# Prompt: <Short Name>

Prompt ID: <UUID or hash>
Status: draft | approved | deprecated
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

This mirrors spec discipline and keeps prompts auditable.

---

3. todo.md Integration Rule

todo.md never embeds long prompts. Instead, use a reference directive:

- [ ] Execute prompt: prompts/prompt-spec-elicitation-auth.md
      Outcome: Generate Spec Elicitation artifacts for auth subsystem

Rules:
- One todo -> one prompt file
- Todo expresses intent, not instructions
- Prompt file is the execution authority

This aligns with existing workflow and task sweep rules.

---

4. Creation Paths (Both Allowed)

A. User-Created Prompt
- User manually adds file under /prompts/
- Adds referencing todo
- Normal execution flow

B. System-Generated Prompt

User instruction:
"Create a prompt file for the following and add a todo referencing it."

System behavior:
1. Write prompt into /prompts/prompt-<slug>.md
2. Add a referencing entry to todo.md
3. Record creation in completed.md when done

No prompt text is duplicated.

---

5. Governance and Enforcement Rules

Hard Rules
- Prompt files are read-only during execution
- Modifying a prompt requires:
  - new commit
  - updated Last-Modified
  - optional new Prompt ID
- Prompts may not bypass specs or synchronizations

Agent Enforcement
- Planner Agent validates referenced prompt exists
- Prompt Optimizer may trim at execution time but never edits the source
- Security Agent reviews prompts touching auth, secrets, or external systems

---

6. Lifecycle Alignment

| Phase | Artifact                         |
| ----- | -------------------------------- |
| Plan  | Prompt file created / referenced |
| Do    | Prompt executed                  |
| Check | Outputs validated                |
| Act   | Prompt revised or deprecated     |

Fully consistent with the Codex operational framework.

---

7. Optional Extension (Later)

Not required now, but compatible:
- prompts/lib/ for reusable prompts
- prompt hashing for tamper detection
- prompt-to-spec linkage (Spec-ID: header)

---

Net Effect

- No clutter in todo.md
- Long prompts become governed artifacts
- Execution remains deterministic
- Zero weakening of CERES constraints

If you want, next step is:
- exact wording to add to AGENTS.md under Workflow and Coordination
- or a migration rule for existing long todos into prompt files

---

Addendum: Prompt Decomposition vs. Monolithic Prompt Execution

This section extends the Externalized Long-Form Prompt Artifacts feature.

Decision Rule (Mandatory)

When a large prompt is introduced, the system must classify it first:

Classification Question (Gate)
"Does this prompt describe one atomic outcome, or multiple separable outcomes?"

This decision is required before writing todo.md entries.

Case A - Decomposable Prompt -> Task Series

Definition
A prompt is decomposable if:
- It requests multiple deliverables that can be completed independently
- It spans multiple phases, concepts, or artifacts
- Partial completion is meaningful

System Behavior
1. Prompt is stored in /prompts/prompt-<slug>.md
2. The system extracts tasks
3. todo.md receives multiple entries, each referencing the same prompt file

Example:
- [ ] From prompt prompts/prompt-ui-constitution.md: Extract UI principles
- [ ] From prompt prompts/prompt-ui-constitution.md: Draft constitution schema
- [ ] From prompt prompts/prompt-ui-constitution.md: Validate against governance rules

Rules:
- Each todo must be independently testable
- All todos reference the same prompt source
- Execution order is explicit if required

This preserves PDCA granularity and avoids hidden batching.

Case B - Atomic but Long Prompt -> Single Task (7-Part Codex Prompt)

Definition
A prompt is atomic if:
- It produces one integrated outcome
- The steps are tightly coupled
- Breaking it apart would introduce ambiguity or loss of intent
- Length is due to precision, constraints, or reasoning depth, not scope

System Behavior
1. Prompt is stored as a standalone file
2. todo.md contains one task only
3. The task executes the full prompt as a unit

Example:
- [ ] Execute prompt: prompts/prompt-spec-elicitation-auth.md
      Outcome: Produce complete Spec Elicitation artifact set

Required Format
In this case, the 7-part Codex prompt structure is mandatory and sufficient:
1. Intent
2. Constraints
3. Scope
4. Inputs
5. Required Reasoning
6. Output Artifacts
7. Validation Criteria

No task decomposition is permitted unless the prompt itself is revised.

Enforcement Rules
- Planner Agent must explicitly label the prompt as:
  - decomposable or atomic
- Mixed behavior is forbidden:
  - No partial decomposition
  - No silent batching
- Reclassification requires:
  - Prompt edit
  - New commit
  - Updated metadata

Summary (Hard Constraints)
- Large does not mean decomposable
- Decomposition is about semantic independence, not length
- Atomic, page-long prompts are valid and governed
- Task explosion is allowed only when justified

This closes the loop:
- Long prompts are cleanly externalized
- Complex work stays auditable
- CERES avoids both clutter and hidden complexity

If you want next:
- Exact language to splice into AGENTS.md
- A validator rule for enforcing the classification
- Or a prompt-author checklist to prevent misuse

5. Required Reasoning
   Provide a concise comparison and identify the missing human-facing layer without restating enforcement rules.
6. Output Artifacts
   Produce a short decision memo at `docs/skills-registry-gap.md`.
7. Validation Criteria
   The memo must state that CERES skills already exist, name the missing human-facing layer, and recommend one of: formalize a shared schema or add a registry projection.

