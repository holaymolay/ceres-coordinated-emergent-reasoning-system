Spec Title: Reasoning Skills Layer v1
Spec ID: 274f6474-44c8-426b-925f-52f31bc31c45
User Story: As a workflow operator, I need a deterministic Reasoning Skills layer so planning only occurs within explicit, enforceable constraints.

Functional Requirements:
- Run the Reasoning Skill pipeline after the Clarification Gate and before the Planner.
- Execute reasoning skills in a fixed, inspectable order defined by `skills/reasoning/pipeline.yaml`.
- Ensure reasoning skills are deterministic, stateless, LLM-agnostic, and non-executing.
- Allow reasoning skills to halt the run when failure conditions trigger.
- Emit structured, machine-parsable logs for reasoning execution order, guarantees, violations, and abort reasons.

Non-functional Requirements:
- Reasoning skills do not generate code, call tools, or modify files.
- Reasoning skill artifacts are reviewable manifests and schemas only.
- No changes to existing agent responsibilities, PDCA enforcement, or security controls.

Architecture Overview:
- Reasoning skill manifests live under `skills/reasoning/` and conform to `skills/reasoning/reasoning-skill.schema.yaml`.
- The pipeline order is defined in `skills/reasoning/pipeline.yaml` and is executed before planning.
- Planner receives only post-pipeline context; reasoning failures halt the run before planning.

Language & Framework Requirements:
- Documentation-only; no runtime code implementation required.

Testing Plan:
- Validate that reasoning manifests include required fields and align to the schema.
- Run `scripts/validate-reasoning-skills.py` after editing manifests or the pipeline.
- Verify governance docs and wiki reflect the pipeline ordering and observability requirements.

Dependencies:
- None.

Input/Output Schemas:
- Input: user request, active spec ID, active Concept manifest, relevant Synchronizations (if any).
- Output: constrained context for planning or an explicit halt with violations.

Clarifications (optional):
- None.

Validation Criteria:
- Reasoning skill schema, manifests, and pipeline are present under `skills/reasoning/`.
- Governance docs describe the Reasoning Skills layer ordering and constraints.
- Observability requirements for reasoning logs are documented.

Security Constraints:
- No external calls or tool execution during reasoning.
- Reasoning skills read context/specs only and do not write files.
