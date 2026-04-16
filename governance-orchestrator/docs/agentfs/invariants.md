# AgentFS Invariants (What Becomes Impossible)

These invariants are enforced at the filesystem boundary. Any violating operation must fail immediately.

## Concept Isolation
- An agent cannot write outside its bound `/concepts/<concept-id>/` directory.
- A Concept manifest cannot be modified after creation.
- `state.json` cannot be written by non-declared handlers.

## PDCA Sequencing
- `do.log` cannot be created or appended without `plan.md`.
- `check.json` cannot be created without `do.log`.
- `act.md` cannot be created without `check.json`.
- Write-once PDCA artifacts cannot be modified or replaced after creation.

## Synchronization Integrity
- Agents cannot write `status.json` under any Synchronization.
- Agents cannot write files other than `payload.json` inside a sync directory.
- A Synchronization manifest cannot be modified after creation.

## Immutability & Audit
- Append-only logs cannot be truncated or overwritten.
- Audit logs are append-only and system-owned; agents cannot delete or modify entries.
- All filesystem operations must emit a log entry with timestamp, agent identity, path, operation, and result.

## Policy & Security
- Policies and schema definitions are read-only to agents.
- Missing or invalid policies result in fail-closed access (no implicit allows).
- Permission escalation is impossible; capabilities are path-scoped and explicit.
