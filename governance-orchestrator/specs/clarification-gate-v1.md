Spec Title: Clarification Gate v1
Spec ID: 39f7c531-630c-401b-b97e-63419334878f
User Story: As a workflow operator, I need a pre-planner clarification gate so ambiguous inputs are resolved before planning begins.

Functional Requirements:
- Run before planning and before any Reasoning Skills pipeline (if enabled).
- Trigger when required inputs are ambiguous, missing, or too broad to safely plan.
- Ask targeted clarification questions and record answers in the active spec under Clarifications.
- Rerun the gate after clarifications; abort if ambiguity persists.

Non-functional Requirements:
- Deterministic gating logic; no code generation or tool execution during clarification.
- Auditability: every clarification is recorded in the governing spec.

Architecture Overview:
- Clarification Gate sits between user input and planning.
- It reads only the active spec and Concept context needed to detect ambiguity.

Language & Framework Requirements:
- Documentation-only; no runtime code required.

Testing Plan:
- Validate documentation changes in governance docs and spec template.
- Manually verify the Clarifications section is present in new specs.

Dependencies:
- None.

Input/Output Schemas:
- Input: user request, active spec, active Concept context.
- Output: updated spec clarifications or explicit halt.

Clarifications (optional):
- Q: <question> A: <answer>

Validation Criteria:
- Clarification Gate documented in governance docs and workflow guide.
- Spec template includes Clarifications section.
- Clarification flow recorded in the adoption guide.

Security Constraints:
- No external calls or file modifications beyond updating the active spec.
- No code execution during the clarification phase.
