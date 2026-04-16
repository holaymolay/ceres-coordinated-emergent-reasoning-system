# AgentFS Migration Plan

This plan rolls out enforcement in staged phases while preserving existing governance semantics.

## Phase 1: PDCA Artifacts Only
**Objective:** Enforce PDCA sequencing and append-only audit logs without Concept or Synchronization isolation.

Deliverables:
- Mount AgentFS with `/pdca/<task-id>/` enforcement (write-once + append-only + sequencing).
- Append-only audit log (`/audit/ops.log`) for every filesystem operation.
- Fail-closed policy engine with PDCA rules and task bindings.

Exit Criteria:
- Attempted PDCA step skipping is denied at the filesystem boundary.
- Audit log captures every operation with required fields.

## Phase 2: Concept Isolation
**Objective:** Enforce Concept jailing and handler-restricted writes.

Deliverables:
- `/concepts/<concept-id>/` isolation with per-agent concept binding.
- Immutable `manifest.yaml` enforcement.
- `state.json` schema validation and handler-only write restrictions.

Exit Criteria:
- Cross-concept writes are denied.
- Non-handler writes to `state.json` are denied.

## Phase 3: Synchronization Gating
**Objective:** Enforce Synchronization contracts as filesystem-mediated exchanges.

Deliverables:
- `/synchronizations/<sync-id>/` layout with immutable `manifest.yaml`.
- Allow agents to write only `payload.json` (write-once, schema-validated).
- `status.json` system-owned, read-only to agents.

Exit Criteria:
- Agents cannot write or modify `status.json`.
- Only `payload.json` is agent-writable in sync directories.

## Rollback Strategy
- Each phase is reversible by unmounting AgentFS and reverting to the underlying filesystem.
- Audit logs are preserved in append-only form for forensic review.
