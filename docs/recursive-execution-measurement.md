# Recursive Execution Measurement & Promotion Decision

## Objective
Assess the impact of approved recursive execution and decide promote / retain / remove.

## Measurement Window
- Duration: fixed observation window (e.g., 1–2 weeks of real usage)
- Scope: runs with approved `execution_escalation_decision` only

## Metrics
- Success rate: escalated tasks completed vs baseline
- Failure modes: budget exceed, governance violation, adapter fail events
- Cost: time/depth budget usage vs declared budgets
- Drift: any governance/observability/security violations
- Outcomes: regressions introduced vs avoided

## Data Sources
- Observability events: `execution_escalation_decision`, `recursive_adapter_enter/step/exit/fail`
- Task outcomes: `completed.md`, Gap Ledger updates
- Performance logs: timing, retries

## Decision Criteria
- Promote if: higher success rate with acceptable cost and zero governance violations
- Retain (optional) if: mixed results; requires more data or guardrails
- Remove if: frequent violations, regressions, or cost outweighs benefit

## Required Actions During Window
- Log every escalation event and adapter event
- Capture evidence for failures (links to artifacts/logs)
- Record baseline comparisons for similar tasks without escalation

## Final Decision Artifact
- Produce a decision note summarizing metrics, risks, and recommendation
- Update governance/docs if promotion or removal is chosen
