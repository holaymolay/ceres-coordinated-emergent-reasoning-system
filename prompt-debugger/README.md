# CERES Prompt Debugger

Pre-governance gate for all prompt intake (todo-inbox/chat). Runs structural checks, classifies intent, assesses risk, and emits a deterministic debug report before anything reaches governance or execution.

## Artifacts
- **Prompt Debug Report** (see `schemas/prompt_debug_report.schema.json`)
- **Objective Contract** schema: `schemas/objective_contract.schema.json`
- **Gap Ledger** schema: `schemas/gap_ledger.schema.json`
- **Task Plan** schema (projects into `todo.md`): `schemas/task_plan.schema.json`
- **Completed entry** schema: `schemas/completed_entry.schema.json`

## Usage
```bash
# From repo root
prompt-debugger/cli.py --prompt-file todo-inbox.md > /tmp/debug_report.yaml
# Or pipe chat text
printf "Refactor README in ui-constitution" | prompt-debugger/cli.py
```

Statuses:
- `approved`: forward to governance
- `needs-clarification`: return report to human (one bounded question at a time)
- `rejected`: block execution; must be rewritten

## Integration contract
1. All intake (file/chat) passes through this CLI.
2. Governance receives both the original prompt and the generated debug report.
3. No silent fixes: if `needs-clarification` or `rejected`, surface `issues` + `suggested_fix` to the user.
4. Same prompt → same decision (deterministic hashing via `prompt_id`).
