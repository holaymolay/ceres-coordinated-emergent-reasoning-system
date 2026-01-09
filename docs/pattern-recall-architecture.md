# Pattern Recall / Observational Memory — Architecture & Data Model
Status: Draft architecture aligned to Constitution §13 and `docs/pattern-recall-enforcement-checklist.md`.
Scope: Observability extension only; non-authoritative; removable with no behavior change.

## Placement & Phase Boundaries
- Entry points: observe, reflect, post-execution analysis, pre-spec context preparation.
- Explicit non-entry: plan, decide, execute, arbitrage. Calls from these phases MUST no-op or fail closed.
- Placement: Observability extension under `observability/patterns/`; not a Concept; no Synchronizations; not referenced by task materialization or routing.

## Data Model (Informational Only)
Artifacts are flat, auditable files (YAML/JSON/NDJSON) under `observability/patterns/`.

- `ProblemRecord`
  - id (ProblemID, stable), title/statement, source (task/spec/prompt), timestamps, provenance (agent/human), inputs (links), observed outcomes (success/fail/partial as facts).
  - Forbidden: ranks, scores, recommendations, priorities.
- `AttemptRecord`
  - id (AttemptID, stable), problem_id, iteration index, approach summary, artifacts produced (links), outcome (fact), evidence refs (tests/logs), environment/context notes.
  - Forbidden: likelihoods, heuristic weights, prescriptive next steps.
- `Classification`
  - problem_id/attempt_id, categories (e.g., failure_mode, domain), tags (controlled list), confidence as bounded qualitative label (optional) only if sourced from evidence; no numeric scoring.
  - Forbidden: ordering keys, preference weights.
- `Relation`
  - from_id, to_id, relation_type (e.g., similar_problem, reused_artifact, conflicting_change), rationale text, evidence refs.
  - Forbidden: recommendation fields or priority edges.

Allowed fields are factual, descriptive, or referential; forbidden fields exclude any prescriptive or prioritization semantics.

## Lifecycle
1) Append-only capture: log `ProblemRecord` + `AttemptRecord` with provenance at observation time.
2) Summarize: generate informational summaries and classifications; never alter originals—write new derived files under `observability/patterns/summaries/`.
3) Recall: lookup by ProblemID/AttemptID/tags to surface past contexts; outputs are read-only views/snippets.
4) Deterministic regeneration: given the same inputs (logs/evidence), summaries and indices must regenerate identically; no learned/opaque state.

## Interfaces (Read-Only Consumers)
- Readers: humans, spec authors, reviewers, observability dashboards.
- Access pattern: explicit fetch of records/summaries by ID or tag; outputs labeled informational-only.
- Forbidden consumers: Planner/Execution/Arbitration unless a spec or human explicitly references a specific record; no automatic feed-in or write-back paths.
- Writes: only the observability layer appends records; no external component may mutate or delete artifacts.

## Removal Proof
- Statement: CERES must boot, plan, and execute identically with the Pattern Recall layer disabled or absent.
- Test plan:
  1) Feature-flag off or remove `observability/patterns/`; run preflight, planning, execution of a sample task—results match baseline.
  2) With layer enabled, run the same task; ensure no task ordering/routing differences and no planner/execution inputs consumed unless explicitly referenced.
  3) Verify failure paths: attempts to invoke from plan/decide/execute/arbitrage phases no-op/fail closed and leave artifacts untouched.
  4) Determinism check: regenerate summaries/indices from the same inputs and confirm identical outputs.
