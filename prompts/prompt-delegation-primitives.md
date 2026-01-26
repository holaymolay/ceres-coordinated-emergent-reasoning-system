# Prompt: Delegation Primitives Governance

Prompt ID: 02f4495e-377c-4a65-8193-f4ba79aa8db0
Classification: decomposable
Status: draft
Owner: user
Created: 2026-01-26T07:22:29Z
Last-Modified: 2026-01-26T08:02:12Z

## Intent
Add governance-first delegation primitives with canonical events, policy contracts, budgets, registry controls, and removability tests.

## Constraints
- Spec-first: create/update specs before code.
- Governance over autonomy: delegation must be rule-driven, not heuristic/learned.
- Observability: delegation must emit a canonical event; fail closed if event cannot be written.
- Human authority preserved: delegation can be disabled globally/per-run/per-spec.
- Reversible/removable: system must still run end-to-end with delegation disabled.
- Single-concept rule: if the repo uses concept folders, scope changes to ONE concept; if unclear, implement in a new isolated "delegation" module and do not touch unrelated features.
- Add tests for all new logic.
- Non-goals: no RL, no reward shaping, no training pipelines; no autonomous token-level dynamic calling; no implicit routing/fallbacks. Delegation must be explicit and logged.

## Task Decomposition Guidance (decomposable only)
- 1) Draft delegation spec artifacts (event schema, policy contract, budget model, registry, removability).
- 2) Implement canonical event emission, policy evaluation, budget accounting, registry enforcement, and reason_code taxonomy.
- 3) Add removability mode and tests (unit + minimal integration if applicable).
- Order: 1, then 2, then 3.

## Prompt Body
### Intent
Add governance-first "Delegation" primitives: explicit delegation events, spec-bound delegation policy contracts, budgets/cost accounting, collaborator registry, and removability tests. Do NOT add any learning/RL behavior.

### Constraints
- Spec-first: create/update specs before code.
- Governance over autonomy: delegation must be rule-driven, not heuristic/learned.
- Observability: delegation must emit a canonical event; fail closed if event cannot be written.
- Human authority preserved: delegation can be disabled globally/per-run/per-spec.
- Reversible/removable: system must still run end-to-end with delegation disabled.
- Single-concept rule: if the repo uses concept folders, scope changes to ONE concept; if unclear, implement in a new isolated "delegation" module and do not touch unrelated features.
- Add tests for all new logic.
- Non-goals (explicitly forbidden):
  - No RL, no reward shaping, no training pipelines.
  - No autonomous token-level dynamic calling behavior.
  - No implicit routing/fallbacks. Delegation must be explicit and logged.

### Scope
Deliverables
1) Spec artifact(s)
- Add a spec document describing:
  - DelegationEvent schema (required fields)
  - DelegationPolicy contract (eligibility gates, scope constraints, post-conditions, replay requirement)
  - Budget model (per run/phase/spec caps; cost attribution)
  - Collaborator registry (allowlist with versioning; no runtime substitution)
  - Removability mode (delegation disabled must still work)

2) Canonical DelegationEvent
- Implement a single canonical event record emitted on every delegation attempt (success or deny).
- Required fields (minimum):
  - event_id, timestamp
  - spec_id, phase_id, run_id
  - caller_model_id, callee_model_id (versioned)
  - reason_code (ENUM only)
  - scope_hash (hash of exact context sent)
  - budget_before, budget_after, cost_units
  - result_hash (hash of returned tokens, or null if denied)
  - policy_version (rule-set version)
- Rules:
  - No event => no delegation (fail closed).
  - Event must record "DENIED" with denial_reason if blocked by policy/budget/registry.

3) DelegationPolicy contract (rule-driven)
- Implement policy evaluation that returns: ALLOW/DENY + reason.
- Must include:
  - Eligibility gates (explicit, spec-declared)
  - Scope constraints (explicit allowlist for what context may be sent; forbid secrets)
  - Post-conditions (basic validation gates; reject outputs that violate constraints)
  - Replay determinism requirement (same inputs + spec + policy_version => same decision)

4) Budgeting + cost accounting
- Implement:
  - budget caps per run, per phase, per spec
  - deterministic cost calculation unit (e.g., tokens, calls, or abstract "cost_units")
  - budget updates must be recorded in events

5) Collaborator registry + stability rules
- Implement an allowlist registry containing:
  - model_id, version, approved_uses/capability_envelope
- Rules:
  - Only registry-approved collaborators can be called.
  - No dynamic substitution. Any change requires updating the registry artifact/version.

6) Removability / degradation
- Implement a global "delegation disabled" mode:
  - All delegation attempts must be denied (with events logged)
  - System continues execution without crashing
- Add tests proving end-to-end flow does not depend on delegation.

7) Minimal reason_code taxonomy
- Implement a small enum set only (no free-text reasons). Include at least:
  - MISSING_KNOWLEDGE
  - LOW_CONFIDENCE_FINAL
  - CONTRADICTION_DETECTED
  - TOOL_FAILURE_RECOVERY
  - SAFETY_SANITIZATION_REQUIRED

Testing requirements
- Unit tests for:
  - policy allow/deny decisions (deterministic)
  - budget enforcement
  - registry enforcement
  - event emission (allow + deny)
  - removability mode
- If repo has integration tests, add one minimal integration test covering "delegation disabled" behavior.
- Ensure lint/tests pass.

Process
- Start by locating existing governance/spec patterns in the repo (specs folder, event logs, manifests).
- Add the spec artifact(s) first.
- Then implement minimal code in an isolated module.
- Then add tests.
- Keep commits atomic and scoped.

### Inputs
- Existing governance/spec patterns, event logs, and manifest schemas.

### Required Reasoning
- Apply spec-first ordering and keep code isolated and reversible.
- Enforce deterministic policy decisions and event emission.

### Output Artifacts
- Spec document(s) describing DelegationEvent, DelegationPolicy, budgets, registry, and removability.
- Canonical DelegationEvent emission on every attempt (allow or deny).
- Policy evaluation, budget accounting, registry enforcement, and removability mode.
- Unit tests and minimal integration test (if applicable).

### Validation Criteria
- Policy decisions are deterministic and replayable.
- Budget, registry, and removability rules are enforced and logged.
- Events are emitted for allow and deny paths with required fields.
- Tests cover allow/deny, budgets, registry, and removability; integration test added if applicable.
- Non-goals are respected (no RL, no implicit routing, no autonomous delegation).

## Validation Criteria
- All deliverables and testing requirements in the prompt body are satisfied.
