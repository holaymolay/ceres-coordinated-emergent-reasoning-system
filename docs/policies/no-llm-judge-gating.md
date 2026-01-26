# Policy: No LLM Judge as Gate

## Rule
LLM-as-judge MUST NOT be used as an enforcement or gating mechanism in CERES.

## Scope
- Applies to all governance, validation, and execution gates.
- Applies to CI, preflight, lifecycle gates, and any formal verification step.

## Allowed Use (Advisory Only)
- LLM judgments may be recorded as advisory notes.
- Advisory notes cannot block, approve, or certify outcomes.

## Rationale
Gates must be deterministic, reproducible, and auditable. LLM judgments are probabilistic and can drift, so they are not eligible for enforcement.

## Compliance
Any proposal that introduces LLM judgment as a gate must be rejected.
