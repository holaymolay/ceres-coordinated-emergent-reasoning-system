# AgentFS Filesystem Layout (Authoritative)

This document defines the only allowed paths and their enforcement semantics. Paths not listed here are denied by default.

## Root Layout
```
/
  concepts/
    <concept-id>/
      manifest.yaml        (read-only, immutable after creation)
      state.json           (schema-validated, write-restricted)
      handlers/            (write-restricted)
      tests/               (write-restricted)
  pdca/
    <task-id>/
      plan.md              (write-once)
      do.log               (append-only; requires plan.md)
      check.json           (write-once; requires do.log; schema-validated)
      act.md               (write-once; requires check.json)
  synchronizations/
    <sync-id>/
      manifest.yaml        (read-only, immutable after creation)
      payload.json         (write-once; agent-writable)
      status.json          (system-owned; agent read-only)
  audit/
    ops.log                (append-only; system-owned)
  policies/
    access-policy.yaml     (read-only; system-owned)
    schemas/               (read-only; system-owned)
```

## Path Semantics (Normative)

### `/concepts/<concept-id>/`
- Agents are jailed to exactly one Concept directory; cross-concept paths are denied.
- `manifest.yaml` is immutable after creation; agents cannot modify it.
- `state.json` is mutable only by handlers declared in the Concept manifest; all writes are schema-validated.
- `handlers/` and `tests/` are writable only by the agent identity bound to the Concept handler declaration; others are read-only.

### `/pdca/<task-id>/`
- `plan.md` is write-once and must exist before any other PDCA file is created.
- `do.log` is append-only and denied unless `plan.md` exists.
- `check.json` is write-once, schema-validated, and denied unless `do.log` exists.
- `act.md` is write-once and denied unless `check.json` exists.
- No PDCA file may be modified after creation (except append-only `do.log`).

### `/synchronizations/<sync-id>/`
- `manifest.yaml` is immutable after creation.
- `payload.json` is write-once and is the only agent-writable file in the sync directory.
- `status.json` is system-owned and read-only to all agents.

### `/audit/`
- All filesystem operations append a record to `ops.log`.
- `ops.log` is append-only and system-owned; agents may read but never write.

### `/policies/`
- Policy and schema files are system-owned and read-only to agents.
- If a policy or schema is missing or invalid, AgentFS fails closed.
