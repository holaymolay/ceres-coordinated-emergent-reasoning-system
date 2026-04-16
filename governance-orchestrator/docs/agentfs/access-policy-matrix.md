# AgentFS Access-Policy Matrix

This matrix defines default path access by agent role. All access is deny-by-default; explicit permissions below are required in addition to concept/task bindings.

## Permission Legend
- `R`: read-only
- `W1`: write-once
- `A`: append-only
- `RW`: read/write (restricted by handler/task ownership)
- `X`: no access
- `S`: system-owned (AgentFS kernel only)

## Roles (from `AGENTS.md`)
- Execution Agent (task owner; includes specialized execution agents)
- Planner / Task Manager
- Coordinator / Router
- Security Agent / Gatekeeper
- Observability Agent / Pruning Agent
- Other Agents (Caching, Arbitration, Memory, Prompt Optimizer)
- AgentFS System (enforcement layer, not an agent)

## Path Matrix

| Path | Execution Agent | Planner / Task Manager | Coordinator / Router | Security / Gatekeeper | Observability / Pruning | Other Agents | AgentFS System |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `/concepts/<concept-id>/manifest.yaml` | R | R | R | R | R | R | S (create-once) |
| `/concepts/<concept-id>/state.json` | RW (handler-only) | R | R | R | R | R | S (schema enforcement) |
| `/concepts/<concept-id>/handlers/` | RW (handler-only) | R | R | R | R | R | S |
| `/concepts/<concept-id>/tests/` | RW (handler-only) | R | R | R | R | R | S |
| `/pdca/<task-id>/plan.md` | W1 (task owner) | R | R | R | R | R | S |
| `/pdca/<task-id>/do.log` | A (task owner) | R | R | R | R | R | S |
| `/pdca/<task-id>/check.json` | W1 (task owner) | R | R | R | R | R | S |
| `/pdca/<task-id>/act.md` | W1 (task owner) | R | R | R | R | R | S |
| `/synchronizations/<sync-id>/manifest.yaml` | R | R | R | R | R | R | S (create-once) |
| `/synchronizations/<sync-id>/payload.json` | W1 (task owner) | R | R | R | R | R | S |
| `/synchronizations/<sync-id>/status.json` | R | R | R | R | R | R | S |
| `/audit/ops.log` | X | X | R | R | R | X | S |
| `/policies/*` | X | X | X | R | R | X | S |

## Notes (Normative)
- Concept jail: any path outside the agent's bound `/concepts/<concept-id>/` is denied, regardless of role.
- Task ownership: PDCA and Synchronization writes require an active task binding for `<task-id>` and `<sync-id>`.
- Handler restriction: `state.json`, `handlers/`, and `tests/` writes are allowed only for identities declared in the Concept manifest.
- System-owned: `S` indicates AgentFS internal operations; agents cannot write these paths under any circumstance.
