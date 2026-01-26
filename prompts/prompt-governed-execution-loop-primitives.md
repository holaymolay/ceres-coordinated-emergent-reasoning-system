# Prompt: Governed Execution Loop Primitives

Prompt ID: aaa1cfa3-1533-46be-b342-c823ce96b662
Classification: decomposable
Status: draft
Owner: user
Created: 2026-01-26T07:22:29Z
Last-Modified: 2026-01-26T08:02:12Z

## Intent
Add opt-in governed execution-loop primitives with policy schema, enforcement, observability, and tests while keeping default behavior unchanged.

## Constraints
- Implement ONLY the approved governed primitives; no raw shell looping, vendor-specific hooks, or persona-driven behavior.
- Execution remains OFF by default; no behavior changes unless explicitly enabled by project policy config.
- No autonomous continuation; continuation must be bounded by config and stop rules.
- No implementation tied to Claude Code internals or Medium article specifics.
- Single-concept / single-area change per commit; keep changes scoped and reversible.

## Task Decomposition Guidance (decomposable only)
- 1) Doctrine update with governed loop primitives and anti-pattern (no code).
- 2) Extend ceres.policy schema and validation rules (default-off).
- 3) Implement Execution Governor with deterministic enforcement and per-iteration decisions.
- 4) Add append-only observability logs with config snapshot hash.
- 5) Add tests and apply version bump if governance/schema/enforcement behavior changes.
- Order: 1, then 2, then 3, then 4, then 5.

## Prompt Body
### Intent
Implement governed execution-loop primitives (opt-in) in CERES without breaking philosophy.

### Constraints
- Implement ONLY the governed primitives approved from the "Ralph Wiggum / Claude Code loop" analysis: explicit termination criteria, hard iteration limits, external termination control, anti-pattern documentation.
- Do NOT implement raw shell looping, vendor-specific hooks, or persona-driven behavior.
- Execution must remain OFF by default.
- Single-concept / single-area change per commit (keep changes scoped and reversible).
- No behavior changes unless explicitly enabled by project policy config.
- No autonomous continuation: all continuation must be bounded by config + stop rules.
- No implementation that depends on Claude Code internals or Medium article specifics.

### Scope
Preconditions (must exist or be created first if missing)
- Layered project config model: ceres.constitution.yaml (immutable) and ceres.policy.yaml (project-level), with clear precedence rules.
- CERES version declaration: ceres.version.yaml (authoritative).
- Semantic versioning + version enforcement gate already documented (do not redesign it).

Deliverables (in order; stop after each deliverable if blocked)
1) Doctrine update (normative):
   - Add a section defining "Governed Execution Loop Primitives":
     * Explicit termination criteria (machine-checkable "completion promise" concept)
     * Hard iteration limits (max_iterations)
     * External termination control (governor decides stop; model cannot self-extend)
   - Add an explicit anti-pattern: "Forced looping without spec/acceptance criteria" (document as misuse risk).
   - State clearly: execution remains OFF by default; enable only via policy config.

2) Policy schema additions (project-level):
   - Extend ceres.policy.yaml schema to include:
     execution.enabled (default false)
     execution.mode (default disabled)
     execution.max_iterations (required when enabled)
     execution.termination.completion_promise (required when enabled)
     execution.pause_every_n_iterations (optional, default conservative)
     execution.failure_behavior (halt_and_report)
   - Add validation rules: missing/ambiguous termination criteria => block execution.

3) Minimal enforcement component (no vendor hooks):
   - Implement an "Execution Governor" that:
     * reads policy config
     * enforces max_iterations
     * enforces "completion_promise" termination only when explicitly emitted
     * halts deterministically on limit/violation
     * emits structured logs for each iteration (iteration number, decision, reason)
   - This governor must be usable by any executor/orchestrator; do not tie to a specific LLM tool.

4) Observability updates:
   - Ensure each iteration produces an auditable record (append-only log/event entry).
   - Include: timestamp, iteration, allowed/blocked, stop reason, config snapshot hash.

5) Tests:
   - Unit tests proving:
     * execution cannot run when disabled
     * missing completion_promise blocks execution
     * iteration cap halts deterministically
     * completion_promise triggers stop
     * violations halt_and_report
   - Tests must be deterministic and not require network calls.

### Inputs
- Existing governance/policy schemas and validation flow.
- Existing observability/logging mechanisms.

### Required Reasoning
- Preserve default-off behavior and reversibility.
- Enforce explicit termination rules and bounded execution.
- Keep changes minimal and aligned with existing governance patterns.

### Output Artifacts
- Implement deliverables in the stated order; stop after each deliverable if blocked.
- Include a version bump if governance/schema/enforcement behavior changes.
- Output format:
  - Provide a short handover note listing:
    * files changed
    * tests run
    * how to enable the feature safely (policy keys)
    * any blocked items

### Validation Criteria
Acceptance criteria
- Default behavior unchanged: execution remains disabled unless policy enables it.
- No infinite loops possible without explicitly setting permissive config (and still bounded by max_iterations).
- Termination is explicit and externally enforced.
- Clear anti-pattern documentation exists.
- Logging makes each iteration explainable.
- Version bump is included if governance/schema/enforcement behavior changes.

## Validation Criteria
- All acceptance criteria and deliverable requirements are satisfied.
