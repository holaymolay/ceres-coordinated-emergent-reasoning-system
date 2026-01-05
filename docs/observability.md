# CERES Observability Approach (Interim)

Decision: keep observability embedded for now with hooks; plan extraction to a dedicated repo later.

## Goals
- Capture metrics, logs, and drift signals for governance/execution runs.
- Ensure execution cannot silence telemetry.
- Provide cross-repo visibility for debugging and audits.

## Interim Hooks (to implement next)
- Emit run receipts (existing) with push hash and outcomes; aggregate centrally.
- Add lightweight logging hooks in governance/execution to record stage transitions and gate outcomes.
- Capture Prompt Debug Reports alongside task records for traceability.
- Add drift checks: validate artifacts against schemas and fail gates on mismatch.

## Extraction Plan (later)
- Stand up `observability` repo with ingestion pipeline, storage, and dashboards.
- Define contract for emitting events (schema + transport) from sub-repos.
- Ensure security/PII posture documented before enabling external sinks.

## Hard Rules
- Telemetry cannot be disabled by execution tasks.
- Governance gates must log pass/fail with reasons.
- Run receipts remain mandatory for every task cycle.
