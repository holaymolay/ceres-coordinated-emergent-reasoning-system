# Prompt: RAM Integration Governance Rules

Prompt ID: 17a63ee3-8764-43d5-a95e-1276cdff06ff
Classification: decomposable
Status: draft
Owner: user
Created: 2026-01-26T07:22:29Z
Last-Modified: 2026-01-26T08:02:12Z

## Intent
Add RAM-inspired integration governance rules, schemas, validators, observability, and documentation as policy-only changes.

## Constraints
- Policy and enforcement hooks only; no weight-level ML mechanics or autonomous merging logic.
- No "generalist creation"; no ML model parameter operations.
- Preserve: spec-first, governance over autonomy, observability over opacity, human authority, reversibility, no hidden agency.
- Use existing governance structure and naming conventions.
- If a "Doctor" / validation / gate mechanism exists, extend it; otherwise create minimal validators consistent with repo patterns.
- Keep changes small and reversible.
- One-concept-per-commit discipline; if multiple concepts would be touched, create/modify a Synchronization contract first.
- Prefer additive changes and feature flags/config toggles for enforcement strictness.
- No broad refactors; no breaking changes without compatibility shims.

## Task Decomposition Guidance (decomposable only)
- 1) Locate manifest/validator touchpoints and extend schemas; add profiling record schema with backward-compatible defaults.
- 2) Implement pre-merge profiling gate, shared/private enforcement, anti-dilution rule, integrity check, and observability events.
- 3) Update docs and reviewer checklist; add tests and provide output summary requirements.
- Order: 1, then 2, then 3.

## Prompt Body
### Intent
Implement four governance-level rules inspired by "Behavior Knowledge Merge in Reinforced Agentic Models" (arxiv:2601.13572) as CERES policy (no weight-level ML mechanics):
1) Shared vs Unique separation
2) Pre-merge profiling gate
3) Anti-signal-dilution doctrine (anti naive averaging/consensus)
4) Staged integration pattern (profile -> classify -> combine)

### Constraints
- Policy + enforcement hooks only (schemas, validators, docs, checklists).
- No autonomous merging logic. No "generalist creation." No ML model parameter operations.
- Must preserve: spec-first, governance over autonomy, observability over opacity, human authority, reversibility, no hidden agency.
- Keep changes small and reversible.
- One-concept-per-commit discipline; if multiple concepts would be touched, create/modify a Synchronization contract first.
- Prefer additive changes and feature flags/config toggles for enforcement strictness.
- No broad refactors. No breaking changes without compatibility shims.

### Scope
- Shared vs unique separation
- Pre-merge profiling gate
- Anti-signal-dilution doctrine (block naive averaging/consensus without justification)
- Staged integration pattern (profile -> classify -> combine)

### Inputs
- Existing governance structure and naming conventions.
- Existing Doctor/validation/gate mechanisms, if present.

### Required Reasoning
- Identify where manifests live and how validations are currently performed.
- Extend existing validators when possible; otherwise add minimal new ones consistent with repo patterns.
- Keep enforcement deterministic, reversible, and auditable.

### Output Artifacts
Deliverables (required)
A) Schema updates
- Add fields to Concept and Synchronization manifests (or equivalent governance artifacts) to declare:
  - shared_surface (explicit list of artifacts/outputs/interfaces eligible for synchronization)
  - private_surface (explicit list of artifacts/outputs/interfaces not eligible for implicit merge)
- Add a "profiling record" artifact schema for cross-concept/agent integration events:
  - identifies participants, artifacts considered, overlap classification, and decision rationale.

B) Governance gates
- Add a mandatory "Pre-merge profiling" gate that runs before any cross-concept/agent combination step.
- Enforce: no aggregation/merge unless profiling artifact exists and declares shared vs unique surfaces.
- Enforce: "anti-dilution" rule -- block or require explicit justification when a step uses averaging/consensus/voting across heterogeneous sources.

C) Observability
- Log profiling and gate outcomes as first-class events (structured, queryable).
- Add a minimal "integrity check" rule: if cross-concept behavior/output changes without a local spec/commit reference, emit a warning event (no auto-fix).

D) Documentation
- Update the governing docs to include:
  - Definitions: shared_surface, private_surface, profiling
  - Prohibitions: naive averaging/consensus without dilution justification
  - Required process: staged integration pattern
- Add a short checklist for human reviewers.

Steps
1) Identify where manifests live and how validations are currently performed.
2) Implement schema extensions + backward-compatible defaults.
3) Implement profiling artifact type + storage location.
4) Add gate/validator checks to the existing pipeline.
5) Add structured event logging.
6) Add tests.
7) Update docs.

Output
- Provide a concise diff summary + file list changed.
- Provide commands to run tests/lint relevant to the changes.

### Validation Criteria
Acceptance criteria (must be objectively checkable)
1) A cross-concept/agent integration attempt without a profiling artifact is blocked (or fails validation) with a clear message.
2) If profiling exists but shared/private surfaces are missing, validation fails.
3) Any use of "vote/average/consensus" style aggregator in governed steps triggers the anti-dilution rule unless an explicit justification field is present.
4) Profiling + gate outcomes are emitted as structured logs/events.
5) Docs updated and consistent with schemas and validations.
6) Tests added for validators/gates (unit-level at minimum).

## Validation Criteria
- All acceptance criteria in the prompt body are met.
- Deliverables and output formatting requirements are satisfied.
