# Prompt: Clarification request governance update

Prompt ID: 62738bbd-95a2-4536-b1da-e6b1b477596c
Classification: atomic
Status: draft
Owner: user
Created: 2026-01-07T08:52:36.981951Z
Last-Modified: 2026-01-07T08:52:36.981951Z

## Intent
Introduce a governance rule that replaces raw questions with structured clarification artifacts.

## Constraints
- Governance-only changes; no code.
- Single-concept change.
- Violations must be blocking and logged.

## Task Decomposition Guidance (decomposable only)
N/A

## Prompt Body
Below is a ready-to-paste Codex prompt.
It is atomic, governance-first, CERES-compliant, and does exactly one thing.

No commentary. This is the artifact.

---

CODEX PROMPT — GOVERNANCE UPDATE

Intent
Introduce a mandatory governance rule that prohibits agents from asking raw questions and enforces structured clarification as a first-class artifact.

Constraints
- Modify governance only (no executable code).
- Single concept change.
- Must be enforceable, auditable, and blocking.
- Must not weaken existing CERES rules.
- Treat violations as a hard failure (same class as vibe coding).

Task
Update CERES governance to add a new rule defining how uncertainty and questions are handled.

Required Changes (exact)
1. Add a new governance rule under the core execution / agent behavior section stating:
   - Agents are forbidden from emitting free-form or conversational questions.
   - Any uncertainty must be expressed as a structured clarification artifact.
   - Raw questions are a blocking governance violation.
2. Define a new first-class artifact named ClarificationRequest with:
   - Required fields:
     - source_agent
     - blocking_reason
     - classification (technical | preference | ambiguity | optional)
     - context (why this answer matters)
     - options (explicit choices or defaults)
     - default (required if user does not respond)
   - Explicit statement that this artifact is user-facing.
3. Update enforcement semantics:
   - If an agent emits a raw question, the run must halt.
   - The violation must be logged via observability.
   - The agent must be instructed to re-emit the question as a ClarificationRequest.
4. Explicitly classify this as an anti-pattern:
   - Name the anti-pattern: Unstructured Question Emission
   - State that it is prohibited for the same reason as vibe coding: ambiguity leakage.

Out of Scope (do not do)
- Do not implement agents.
- Do not add execution code.
- Do not refactor unrelated governance text.
- Do not introduce optional language ("should", "recommended").

Validation Criteria
- Governance text clearly bans raw questions.
- A reader can unambiguously determine:
  - what is allowed
  - what is forbidden
  - what happens on violation
- The change is minimal, explicit, and auditable.
- No other concepts are modified.

Output Format
- Provide exact governance text additions or diffs.
- Clearly indicate insertion points.
- No explanations outside the governance text.

---

If you want the next prompt, it should be:
"Implement the Clarification Agent in strict compliance with the new governance rule."

Do not reverse the order.


## Validation Criteria
- Governance bans raw questions and defines ClarificationRequest fields.
- Enforcement semantics specify halt + observability + re-emit requirement.
- Anti-pattern is explicitly named and prohibited.
