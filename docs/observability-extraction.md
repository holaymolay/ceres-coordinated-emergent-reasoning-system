# CERES Observability Extraction Plan

Goal: Move from embedded hooks to a dedicated observability repo once hooks exist across components.

Steps:
1) Standardize emission: use `scripts/log_event.py` (hub) from governance/execution for gates and stages.
2) Define event schema (type/status/context) and required fields (task_id, repo, commit, gap_id optional).
3) Create `ceres-observability` repo with:
   - ingestion (JSONL → store)
   - storage (S3/blob or local for now)
   - dashboards/queries
4) Add client shim in each component to POST or append to a queue; keep `log_event.py` as fallback.
5) Security/PII posture: define classification, allowed sinks, retention.
6) Gradual rollout: mirror JSONL locally, then enable remote sink behind a flag.
