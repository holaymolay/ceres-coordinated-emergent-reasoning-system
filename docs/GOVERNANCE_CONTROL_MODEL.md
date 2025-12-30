# Governance Control Model

## Descriptive vs Control Artifacts
- **Descriptive**: Capture intent, context, and design rationale (e.g., specs, concepts, ledgers). They inform decisions but do not block execution by themselves.
- **Control**: Enforce explicit constraints (schemas, validators, CI rules) that can stop a change until it complies.

## PID-Lite Governance Loop
- **Plan**: Declare desired state and guardrails in descriptive artifacts.
- **Act**: Execute within declared controls; apply only the minimal hard gates required for safety and contract validity.
- **Check**: Measure outcomes against contracts, schemas, and acceptance criteria.
- **Adjust**: Tune controls when they cause drift or friction; avoid escalating gates beyond the anti-windup limits.

### Anti-Windup Limits
- `max_blocking_gates_per_PR = 2`
- `max_retries_per_task = 2`
- `max_human_overrides_per_PR = 1`

If these limits are exceeded, pause and reassess the control settings instead of adding more gates.

### Demotion Rule
Repeated non-safety violations trigger demotion of the offending control from hard gate to advisory until it is corrected. Safety-critical gates remain hard.

### Hard-Gating Guidance
- Contract validity **may** hard-gate (e.g., schema validity, missing required artifacts).
- Subjective style or taste **must not** hard-gate; keep them advisory only.
