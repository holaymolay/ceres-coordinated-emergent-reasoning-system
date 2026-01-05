# Canonical Layer Model (Execution Stack)

This is a vertical execution stack, not a repo taxonomy.

## 0. Interface Layer
**What enters the system**
- Human (CLI, VS Code, todo inbox, voice, raw text)
- External triggers (webhooks, schedulers, future MCP servers)

Output:
- Unstructured or semi-structured intent

Purpose:
- Accept messy reality
- No correctness assumptions

Primary artifact: Intake record (`todo-inbox.md` entry or raw prompt).
Entry criteria: New external input received.
Exit criteria: Input captured as a distinct intake record with provenance.

---

## 1. Intake & Normalization Layer
**Make intent legible**

Responsibilities:
- Parse raw input
- Normalize into a candidate Objective
- Strip noise, preserve ambiguity

Artifacts:
- Draft Objective
- Initial metadata (source, urgency, scope guess)

Key rule:
- Objectives are explicitly non-binding

Primary artifact: Objective Contract (draft).
Entry criteria: Intake record exists.
Exit criteria: Draft objective recorded with source metadata and ambiguity preserved.

---

## 2. Inference & Gap Analysis Layer
**Are we allowed to proceed?**

Responsibilities:
- Assess readiness
- Detect missing constraints
- Identify ambiguity, risk, or scope bleed

Outputs:
- Readiness status: Ready | Incomplete | Blocking
- Gap Ledger (explicit questions / unknowns)

Hard constraint:
- No planning allowed until blocking gaps are resolved

Primary artifact: Gap Ledger.
Entry criteria: Objective Contract (draft) exists.
Exit criteria: Readiness status set; blocking gaps resolved or explicitly deferred with assumptions.

---

## 3. Planning / Decomposition Layer
**Planner / Task Manager lives here**

Responsibilities:
- Break objective into tasks
- Enforce one-concept-per-task
- Decide sequencing and dependencies

Artifacts:
- Task list
- Concept mapping
- Synchronization requirements (if cross-concept)

This layer produces work, not code.

Primary artifact: Task Plan (`todo.md`).
Entry criteria: Objective Contract committed and Gap Ledger has no blocking gaps.
Exit criteria: Task Plan decomposed with concept mapping, dependencies, and acceptance criteria.

---

## 4. Governance & Arbitration Layer
**Who is allowed to act?**

Agents:
- Coordinator
- Router
- Arbitration Agent
- Gatekeeper

Responsibilities:
- Task routing
- Conflict resolution
- Priority ordering
- Scope enforcement

Key invariant:
- Nothing executes without passing governance

Primary artifact: Governance decision record (`memory.md`).
Entry criteria: Task Plan exists.
Exit criteria: Tasks authorized and assigned; execution permission granted.

---

## 5. Execution Layer
**Actual doing**

Agents:
- Codex / Claude Code / Gemini Code
- Specialized agents (UI, DB, infra, etc.)

Hard rules:
- Single Concept per commit
- No cross-concept writes without Synchronization
- Spec + manifest injected every run

Outputs:
- Code
- Logs
- Tests
- Diffs

Primary artifact: Change set + evidence (diff/commit with links).
Entry criteria: Governance authorization and active task marked in-progress in `todo.md`.
Exit criteria: Task completed with evidence captured and changes scoped to the task.

---

## 6. Verification & Validation Layer
**Did reality match intent?**

Responsibilities:
- Tests
- Linting
- Security checks
- Spec conformance

Artifacts:
- Pass/fail signals
- Coverage deltas
- Risk notes

No silent failures allowed.

Primary artifact: Verification evidence (tests/lint/scan outputs referenced in `completed.md`).
Entry criteria: Execution outputs produced.
Exit criteria: Verification results recorded; failures reopen gaps or block completion.

---

## 7. Observability Layer
**System-wide memory of behavior**

Agent:
- Observability Agent

Responsibilities:
- Log everything meaningful
- Capture agent actions, sync invocations, errors, latency, drift indicators

This layer is orthogonal; it watches all layers.

Primary artifact: Observability log events (`logs/events.jsonl`).
Entry criteria: Any meaningful layer activity occurs.
Exit criteria: Event logged with type/status/context.

---

## 8. Persistence & Memory Layer
**Continuity across time**

Agent:
- Memory Agent

Stores:
- Task state
- Decisions
- Context fragments
- Lessons learned

Purpose:
- Prevent reset-to-zero behavior
- Enable replay and auditability

Primary artifact: Memory ledger (`memory.md`).
Fallback export: `handover.md`.
Entry criteria: Verified outputs or decisions exist to persist.
Exit criteria: Updated memory record stored for future runs.

---

## 9. Feedback / PDCA Layer
**System self-correction**

Responsibilities:
- Close the loop (Plan -> Do -> Check -> Act)
- Update specs
- Refine prompts
- Adjust governance

Artifacts:
- `completed.md`
- `lessons_learned.md`
- Updated manifests

Primary artifact: Completed Entry (`completed.md`).
Entry criteria: Verification results recorded.
Exit criteria: Completed Entry recorded and feedback applied to specs/governance as needed.
