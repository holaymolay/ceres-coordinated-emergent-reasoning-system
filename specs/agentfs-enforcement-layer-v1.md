Spec Title: AgentFS Enforcement Layer v1 (Filesystem-Backed Governance)
Spec ID: ac7a3716-e70c-42f7-8a77-18c084943f5b
User Story: As a workflow operator, I need a filesystem-backed enforcement layer that encodes existing governance rules so agent actions are structurally constrained and auditable without relying on prompt discipline.

Functional Requirements:
- Provide a virtual filesystem (AgentFS) that enforces read-only, write-once, append-only, namespace isolation, and per-path access rules.
- Enforce Concept isolation via `/concepts/<concept-id>/` jailing; block cross-concept writes.
- Enforce PDCA sequencing via `/pdca/<task-id>/` with write-once artifacts and append-only logs.
- Enforce Synchronization boundaries via `/synchronizations/<sync-id>/` with agent-writeable payloads and system-owned status.
- Emit append-only audit logs for every filesystem operation (timestamp, agent identity, path, operation, result).
- Keep governance semantics aligned with `AGENTS.md` (no weakening, no new agent roles).
- Keep enforcement LLM-agnostic, deterministic, and auditable.

Non-functional Requirements:
- Deterministic policy enforcement: identical inputs and operations yield identical decisions.
- Fail-closed behavior on missing policies, unknown agents, or invalid paths.
- Auditable logs must be append-only and replayable end-to-end.
- Policy/mechanism separation: enforcement logic and policy definitions are isolated.
- No coupling to a specific LLM provider or SDK.

Architecture Overview:
- Authoritative artifacts (must exist and stay in sync):
  - Filesystem layout specification: `docs/agentfs/filesystem-layout.md`.
  - Access-policy matrix: `docs/agentfs/access-policy-matrix.md`.
  - Invariant list: `docs/agentfs/invariants.md`.
  - Minimal reference implementation (pseudocode): `docs/agentfs/reference-implementation.md`.
  - Migration plan: `docs/agentfs/migration-plan.md`.
- AgentFS sits between agents and the repository; all reads/writes are mediated by policy checks and logged.
- Policy inputs include Concept manifests, handler declarations, PDCA task ownership, and Synchronization manifests.

Language & Framework Requirements:
- Language-agnostic reference implementation; no provider-specific dependencies.
- Implementation may use a FUSE-like abstraction or equivalent virtual filesystem layer.

Testing Plan:
- Policy tests: attempt disallowed reads/writes and confirm fail-closed errors.
- PDCA sequencing tests: ensure `do.log` is blocked before `plan.md`, `check.json` blocked before `do.log`, and `act.md` blocked before `check.json`.
- Concept isolation tests: verify cross-concept write attempts are denied.
- Synchronization tests: verify agents cannot write `status.json` and cannot write outside declared synchronizations.
- Audit tests: every operation produces an append-only log entry with required fields.

Dependencies:
- Schema validation for JSON/YAML (Concept manifests, Synchronization manifests, `check.json` validation).
- Virtual filesystem layer (FUSE-like or kernel-assisted VFS interface).

Input/Output Schemas:
- `concepts/<concept-id>/state.json` schema (Concept-defined, validated by AgentFS).
- `pdca/<task-id>/check.json` schema (PDCA validation contract).
- `synchronizations/<sync-id>/payload.json` schema (Synchronization-defined).
- Audit log schema: `timestamp`, `agent`, `path`, `operation`, `result`, `error`.

Validation Criteria:
- AgentFS blocks cross-concept writes and immutable artifact modification.
- PDCA artifacts enforce required sequencing and write-once/append-only rules.
- Synchronization writes are limited to `payload.json`; `status.json` is system-owned.
- Audit logs are append-only and replayable with complete operation coverage.
- All required artifacts exist in `docs/agentfs/`.

Security Constraints:
- Enforce least privilege and explicit allowlists per agent identity.
- Agents cannot modify policies or audit logs.
- No external calls are required or permitted to enforce filesystem rules.
