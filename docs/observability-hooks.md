# CERES Observability Hooks (Practical)

Use the hub helper `scripts/log_event.py` to log stage transitions and gate outcomes. Append JSONL to `logs/events.jsonl`.

Examples:
- Governance lifecycle gate: `scripts/enforce-lifecycle.py ... --log-helper ../scripts/log_event.py --task-id T-123` (already supported in governance-orchestrator).
- Component stage logging: `scripts/log_event.py --type stage --status pass --message "spec generation" --context '{"task":"T-123"}'`.
- Gate failures: pass `--status fail` and include `failures` array in context.

Conventions:
- type: gate | stage | check | info
- status: pass | fail | warn | info
- context: include task_id, repo, commit hash, gap_id where applicable.

Mandatory rules:
- Execution cannot silence telemetry; log gate pass/fail.
- Use run receipts as before; this helper is additive.
