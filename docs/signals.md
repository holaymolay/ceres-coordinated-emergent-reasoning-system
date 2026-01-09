# Signals Layer (Governance)
Status: Governance definition for the Signals/Notification layer. Informational-only; non-authoritative.

## Purpose
- Surface observable conditions (configuration, integrity, drift, overdue rituals) as notifications.
- Improve operator awareness without changing execution flow or governance decisions.
- Provide auditable evidence that can be consumed by humans or downstream artifacts (e.g., Self-Audit), never by planners/executors implicitly.

## Authority Boundaries
- Informational-only: Signals cannot rank, recommend, prioritize, block, schedule, or mutate plans/specs/prompts/execution paths.
- Non-authoritative: Removal must not affect CERES behavior (Constitution §5 Artifacts; §13 Observational Memory non-authority).
- Phase limits: Emit/read in observe/reflect/pre-spec context; no influence on plan/decide/execute/arbitrate.

## Allowed Inputs
- Doctor findings (read-only evidence about workspace/core lock/config state).
- Explicit configuration state (feature flags, mode/profile, timestamps).
- Observability records (e.g., events.jsonl) for summarization.

## Allowed Outputs
- CLI notices/structured text.
- Append-only records (e.g., `.ceres/workspace/events.jsonl`) with timestamped, human-auditable entries.
- Optional machine-readable summaries for human/spec reference (never auto-consumed by planners/executors).

## Prohibitions
- No actions, auto-fix, auto-migrate, auto-schedule, or blocking behavior.
- No ranking/scoring/recommendation fields.
- No implicit consumption by Planner/Execution; any use must be via explicit human/spec reference.
- No state mutation outside append-only logs.
