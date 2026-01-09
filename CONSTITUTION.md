# CERES Constitution

CERES - Coordinated Emergent Reasoning System - is the canonical umbrella for this ecosystem. It replaces human-centered coordination and judgment with a governed, closed-loop, agentic process for solving complex problems. All components operate under this Constitution.

---

## 1) Authority Model
- **Umbrella (CERES):** decides coordination and reasoning semantics; sets invariants.
- **Governance/Orchestration:** enforces scope, staging, arbitration, and validation; cannot execute scope changes.
- **Execution/Runtime:** obeys approved tasks only; no authority over scope or routing.
- **Subsidiaries:** specs, UI constitutions, pattern registries, observability, security - all subordinate to CERES.

---

## 2) Lifecycle (governed flow)
1. **Objective Intake** - capture raw input and provenance; no interpretation.
2. **Spec Elicitation** - structured interrogation; produce the Spec Elicitation Record; must terminate before inference, planning, or execution.
3. **Objective Contract (draft -> committed)** - goal, constraints, success criteria, allowed sources.
4. **Inference Phase** - readiness check; Gap Ledger creation; resolution strategy selection (ask/infer/prototype/assume with risk).
5. **Planning** - deterministic Task Plan; tasks materialized in `todo.md`; no execution before this exists.
6. **Controlled Prototyping** - explicitly tagged exploratory artifacts only to collapse uncertainty; cannot silently change scope.
7. **Lock-In Moment** - commit Objective + Plan; reject unconfirmed assumptions or elevate for approval.
8. **Execution (PDCA)** - task-by-task obedience; evidence captured; reopen gaps on failure.
9. **Verification** - tests/validation; updates to artifacts; audit trail in `completed.md`.

---

## 3) Inference Phase Model (explicit)
- Phases and constraints are defined in `governance/inference-phases.yaml`.
- Agents may act only in phases listed for their role (see `AGENTS.md`).
- Phase violations are governance failures resolved by Arbitration and blocked by Security.

---

## 4) Interaction Protocol (attention-bounded)
- One decision per turn; tie each clarification to a Gap ID and rationale.
- Raw questions are forbidden; uncertainty must be expressed as a `ClarificationRequest` artifact.
- `ClarificationRequest` must be bounded with explicit options and a default; no free-form prompts.
- Show compressed state before asking: decided, undecided, current gap, consequence.
- Progressive disclosure only; no multi-part or speculative sidebars.
- Explicit pause points after answers; no automatic cascades without policy.

---

## 5) Artifacts (authoritative)
- **Inference Phase Model:** `governance/inference-phases.yaml` (phase constraints).
- **Agent Registry:** `AGENTS.md` (canonical agent roles + pattern permissions).
- **Spec Elicitation Record:** `specs/elicitation/<spec-id>.md` with readiness fields.
- **ClarificationRequest:** user-facing artifact with required fields: source_agent, blocking_reason, classification (technical|preference|ambiguity|optional), context, options, default.
- **Objective Contract:** goal, constraints, success criteria, allowed sources, risk profile.
- **Gap Ledger:** `gap_id`, type, blocking, answerable_by_system, resolution_method, confidence_required, status, evidence_links/assumptions (with risk + expiry).
- **Task Plan -> `todo.md`:** sequenced tasks with concept/phase/acceptance; execution gate.
- **Prompt Artifacts:** `prompts/prompt-<slug>.md` with Prompt ID, status, classification, owner, timestamps; referenced from `todo.md` for long-form execution prompts.
- **Synchronizations:** `synchronizations/*.yaml` validated against `schemas/synchronization.schema.json`.
- **Memory Records:** `memory/records/*.json` validated against `schemas/memory-record.schema.json`.
- **Memory Summary:** `memory.md` is a human-readable summary derived from memory records.
- **Observability Events:** `logs/events.jsonl` validated against `schemas/observability-event.schema.json`.
- **Audit -> `completed.md`:** immutable log of completed tasks with evidence references.
- **Prompt Debug Report:** YAML with prompt_id, status, detected_intent, scope, risk_level, issues, suggested_fix, decision_rationale; required for all intake before governance.
- **Assumptions:** explicit, time-bound, risk-rated; never silent.

---

## 6) Enforcement Rules (non-negotiable)
- No inference, planning, or execution before a Spec Elicitation Record exists, blocking unknowns are resolved, and readiness is declared.
- No execution before Task Plan exists in `todo.md` and is stable/visible.
- Long-form prompts must be externalized in `prompts/prompt-<slug>.md`; `todo.md` references the prompt file and does not embed long prompts.
- Prompt artifacts are read-only during execution; edits require a new commit and updated metadata (Last-Modified, status, and classification as needed).
- Prompt classification is mandatory before planning tasks: `atomic` (single task, 7-part structure) or `decomposable` (multiple tasks referencing the same prompt).
- Agents must comply with `governance/inference-phases.yaml` and `AGENTS.md` (phase + pattern permissions).
- Reflection is mandatory for task classes listed in `governance/inference-phases.yaml`.
- Gap resolution requires evidence, user answer, or explicit assumption with risk/expiry.
- Raw questions are prohibited; uncertainty must be emitted as a `ClarificationRequest`.
- Emitting a raw question halts the run, emits an observability violation, and requires re-emission as `ClarificationRequest`.
- One-question-per-turn protocol enforced via `ClarificationRequest`; non-compliant requests are rejected.
- Prompt Debugger gates all intake (file or chat) before governance; no silent auto-fixes.
- Preflight required: run `scripts/preflight.sh --mode execute` before any execution (Prompt Debugger + lifecycle gate).
- No cross-repo changes without explicit coordination.
- Execution cannot bypass observability/security; telemetry cannot be silenced.
- Observability events must conform to the event schema; nonconformant events are violations.
- Push required before closing a task; record the push hash in `completed.md` (auto-push may be used when safe).
- No credentials in the repo; only placeholder values in env template files (e.g., `.env.example`).
- Same prompt -> same decision; deterministic behavior over permissiveness.

---

## 7) Prohibited Anti-Pattern: Vibe Coding
- **Definition:** code generation or execution without a bound, approved spec.
- **Rule:** vibe coding is a governance violation; agents must refuse to proceed when detected.
- **Non-override:** human preference does not override this rule.

---

## 8) Prohibited Anti-Pattern: Unstructured Question Emission
- **Definition:** emitting raw or conversational questions instead of a `ClarificationRequest`, leaking ambiguity into execution.
- **Rule:** prohibited for the same reason as vibe coding; agents must halt and re-emit as a `ClarificationRequest`.

---

## 9) Naming & Scope
- Umbrella name is **CERES - Coordinated Emergent Reasoning System** (canonical; no aliases above it).
- Subcomponents are CERES subcomponents; they must not redefine coordination or reasoning semantics independently.
- If a parent framework is proposed above CERES, reject; CERES is top-level.

---

## 10) Replacement Clause
- This Constitution supersedes any temporary bootstrap text.
- `PROMPTLOADER.md` must point here; if it diverges, this Constitution prevails.
- Updates to this Constitution must be explicit and versioned; no implicit drift.

---

## 11) Next Step Options
1. Update PROMPTLOADER.md to point here and remove temporary content.
2. Update sub-repo docs to reflect CERES naming and authority.
3. Implement Prompt Debugger and artifact schemas per this Constitution.
