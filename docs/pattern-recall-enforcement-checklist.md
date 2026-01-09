# Pattern Recall / Observational Memory — Enforcement Checklist
Status: Binding checklist for Constitution §13 (Non-Authoritative Pattern Recall / Observational Memory).

- [ ] Authority boundary: Outputs are labeled informational-only; Planner/Execution ingestion paths are disabled by default. Any use must be via explicit human/spec reference (artifact link or prompt id), never implicit.
- [ ] Phase gating: Hooks only run in observe/reflect/post-execution analysis/pre-spec prep. Hard fail or no-op in plan/decide/execute/arbitrage phases.
- [ ] Output constraints: No ranks/scores/recommendations/priorities/rewrites. Records are facts, summaries, classifications, and retrieval indices only.
- [ ] Dependency isolation: CERES must boot/plan/execute identically with the layer removed or disabled (no routing, gating, or task materialization dependencies).
- [ ] Artifact auditability: Flat files only; deterministic regeneration; provenance fields present (who/when/source/task/spec). No opaque stores.
- [ ] Governance review: Any change touching this layer (schema, hooks, ingestion, retrieval) requires explicit governance/observability review before merge.
