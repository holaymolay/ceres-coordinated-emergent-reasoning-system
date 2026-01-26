# Prompt: PSN-Style Safety Insulation Gates

Prompt ID: b8150e3c-b6ce-4064-b21a-61f321b5a90c
Classification: decomposable
Status: draft
Owner: user
Created: 2026-01-26T07:22:29Z
Last-Modified: 2026-01-26T08:02:12Z

## Intent
Implement governance-first insulation against trace integrity failures, refactor scope creep, and shallow regression windows.

## Constraints
- Spec-first: create/extend a spec artifact before code changes.
- Determinism: all gates must be rule-based and reproducible.
- Observability: every decision must emit structured logs/events.
- Human authority preserved: proposals are artifacts; gates decide.
- Reversible/removable: each mechanism independently disable-able.
- Do not modify unrelated modules. Keep diffs small and scoped.
- Add tests for every new gate (unit + at least one integration-style test).
- No hidden autonomy. No background agents. No broad refactors.

## Task Decomposition Guidance (decomposable only)
- 1) Locate touchpoints and add a spec \"Touchpoints\" note with trace schema.
- 2) Implement trace completeness validator and diff-vs-executed-nodes gate.
- 3) Implement refactor scope gate, whitelist enforcement, equivalence checks, and repair/refactor exclusivity.
- 4) Implement regression window tiers, quarantine activation, and rollback behavior.
- 5) Add structured events, tests (unit + integration), and governance doc updates.
- Order: 1, then 2, then 3, then 4, then 5.

## Prompt Body
### Intent
Implement governance-first insulation against three risks: (1) trace integrity failures, (2) refactor scope creep changing behavior, (3) shallow regression windows missing long-tail failures.

### Constraints
- Spec-first: create/extend a spec artifact before code changes.
- Determinism: all gates must be rule-based and reproducible.
- Observability: every decision must emit structured logs/events.
- Human authority preserved: proposals are artifacts; gates decide.
- Reversible/removable: each mechanism independently disable-able.
- Do not modify unrelated modules. Keep diffs small and scoped.
- Add tests for every new gate (unit + at least one integration-style test).
- No hidden autonomy. No background agents. No broad refactors.

### Scope
Tasks (produce and commit in small atomic steps)
1) Locate CERES governance / execution / observability entrypoints.
   - Identify where traces are produced/recorded, where patches are applied, where refactors occur (or would occur), and where gating decisions can be enforced.
   - Output a short "Touchpoints" note in the spec with file paths.

2) Add Trace Integrity Insulation (Trace Completeness Gate)
   - Define a strict trace schema (minimum required fields):
     { trace_id, artifact_id, artifact_version, invocation_order, inputs, outputs, decision_points, executed_nodes, non_executed_nodes, timestamps }
   - Implement a validator that marks traces COMPLETE/INCOMPLETE with explicit reasons.
   - Enforce: no "repair" or "refactor" can proceed unless the trace is COMPLETE.
   - Enforce: any proposed diff must only touch artifacts/nodes present in executed_nodes; if diff touches anything outside -> reject with logged reason.
   - Add "negative space" logging: explicitly record non_executed_nodes.

3) Add Refactor Scope Insulation (Structural-only + Whitelist)
   - Introduce change classification: { REPAIR | REFACTOR } required on every proposal.
   - Enforce: REFACTOR cannot change behavior:
     - no signature changes, no side-effect changes, no control-flow semantic changes.
   - Implement a canonical refactor whitelist (bounded set):
     - duplication merge, common subskill extraction, wrapper/specialization rewrite, call substitution for existing identical behavior, dead branch prune (only if provably unreachable on existing traces).
   - Any refactor outside whitelist -> reject with logged reason.
   - Require a "pre/post equivalence check" on existing trace set:
     - same inputs -> same outputs, same side-effect markers (where available).
     - If equivalence cannot be established on the trace set -> reject.
   - Ensure refactor and repair cannot be combined in one change set.

4) Add Regression Window Insulation (Tiered Validation + Auto Rollback)
   - Implement three validation tiers for any accepted REFACTOR:
     A) Immediate: replay/verify recent affected traces.
     B) Historical: replay/verify last known passing ("golden") traces for touched artifacts.
     C) Spec-edge: boundary/edge traces (if present; otherwise require explicit "missing edge traces" notice and treat as higher risk).
   - Enforce monotonic safety: refactor must not reduce pass rate on ANY previously passing trace in tiers A/B.
   - Add quarantine activation: refactor lands as INACTIVE for one cycle and only activates after passing a second validation run.
   - Add automatic rollback: if thresholds violated, revert immediately using recorded inverse operations; write an auditable rollback record.

5) Observability
   - Emit structured events for:
     trace validation result, diff-vs-executed-nodes check, refactor whitelist decision, equivalence check result, tiered validation results, quarantine activation, rollback trigger.
   - Ensure events include stable IDs and are searchable.

6) Tests
   - Unit tests:
     - trace schema validator (complete vs incomplete)
     - diff-touch-outside-executed-nodes rejection
     - refactor whitelist enforcement
     - repair/refactor mutual exclusivity
     - monotonic safety rule
   - Integration-style test:
     - simulate a refactor proposal that passes immediate but fails historical -> must rollback and emit events.
     - simulate incomplete trace -> must block any proposal.

Deliverables
- A new/updated spec document describing the gates, invariants, and failure modes.
- Minimal code changes implementing gates + observability events.
- Tests passing.
- Update repo docs: a short "Safety Insulation" section in governance docs explaining the gates (no design narrative, just rules).

### Inputs
- Existing CERES governance, execution, observability entrypoints.
- Current trace recording and proposal/gating mechanisms.

### Required Reasoning
- Keep diffs small and scoped to governance/observability touchpoints.
- Maintain determinism and reversibility in all gates.

### Output Artifacts
- List changed files.
- Summarize gates added (1-2 lines each).
- Paste command(s) to run tests.

### Validation Criteria
- Trace completeness gate blocks repairs/refactors on incomplete traces.
- Diffs touching outside executed_nodes are rejected with logged reasons.
- Refactor whitelist and repair/refactor exclusivity are enforced.
- Tiered validation, quarantine activation, and rollback behavior are implemented.
- Required structured events are emitted and searchable.
- Unit and integration tests cover the required cases.

## Validation Criteria
- All acceptance criteria and deliverable requirements are satisfied.
