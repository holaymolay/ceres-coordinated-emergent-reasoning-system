# AgentFS Minimal Reference Implementation (Pseudocode)

This reference is implementation-agnostic. It separates policy from mechanism and assumes a FUSE-like virtual filesystem.

## 1. Policy Model (Declarative)

```text
PolicyStore:
  access_matrix: list of (path_pattern, role, permission)
  concept_bindings: agent_id -> concept_id
  task_bindings: agent_id -> task_id
  handler_bindings: concept_id -> allowed_handler_identities
  schemas:
    state_json: concept_id -> schema
    check_json: task_id -> schema
    sync_payload: sync_id -> schema
```

## 2. Mechanism (Filesystem Adapter)

```text
AgentFS.open(path, mode, agent_ctx):
  decision = PolicyEngine.authorize(agent_ctx, path, mode)
  if not decision.allowed:
    Audit.log(agent_ctx, path, mode, "deny", decision.reason)
    raise EACCES

  if mode is WRITE_ONCE and File.exists(path):
    Audit.log(agent_ctx, path, mode, "deny", "write-once violation")
    raise EACCES

  if mode is APPEND_ONLY and not File.is_append(path):
    Audit.log(agent_ctx, path, mode, "deny", "append-only violation")
    raise EACCES

  return FileHandle(path, mode, agent_ctx)

AgentFS.write(handle, data):
  PolicyEngine.enforce_sequence(handle.agent_ctx, handle.path)
  PolicyEngine.validate_schema(handle.agent_ctx, handle.path, data)
  File.write(handle.path, data, handle.mode)
  Audit.log(handle.agent_ctx, handle.path, handle.mode, "allow", "")
```

## 3. Policy Engine (Checks + Sequencing)

```text
PolicyEngine.authorize(ctx, path, mode):
  if not path.matches_any(PolicyStore.access_matrix for ctx.role):
    return Deny("no matching policy")

  if path.starts_with("/concepts/"):
    if ctx.concept_id != path.concept_id:
      return Deny("concept jail")

  if path.starts_with("/pdca/"):
    if ctx.task_id != path.task_id:
      return Deny("task binding required")

  if path.starts_with("/synchronizations/"):
    if ctx.task_id not in ctx.allowed_syncs:
      return Deny("sync binding required")

  return Allow()

PolicyEngine.enforce_sequence(ctx, path):
  if path == "/pdca/<task-id>/do.log" and not File.exists("plan.md"):
    raise EACCES("plan.md required")
  if path == "/pdca/<task-id>/check.json" and not File.exists("do.log"):
    raise EACCES("do.log required")
  if path == "/pdca/<task-id>/act.md" and not File.exists("check.json"):
    raise EACCES("check.json required")

PolicyEngine.validate_schema(ctx, path, data):
  if path.ends_with("state.json"):
    Schema.validate(PolicyStore.schemas.state_json[ctx.concept_id], data)
  if path.ends_with("check.json"):
    Schema.validate(PolicyStore.schemas.check_json[ctx.task_id], data)
  if path.ends_with("payload.json"):
    Schema.validate(PolicyStore.schemas.sync_payload[path.sync_id], data)
```

## 4. Audit Log (Append-Only)

```text
Audit.log(ctx, path, mode, result, reason):
  entry = {
    "timestamp": now_utc(),
    "agent": ctx.agent_id,
    "path": path,
    "operation": mode,
    "result": result,
    "error": reason
  }
  File.append("/audit/ops.log", json_encode(entry))
```

## 5. Notes (Normative)
- All decisions occur before filesystem mutation.
- Agent identity and bindings are provided by the AgentFS runtime, not by agents.
- Policy files and schemas are loaded read-only and validated at mount time; missing policy fails closed.
