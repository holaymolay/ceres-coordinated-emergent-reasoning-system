# CERES Constitution

CERES — Coordinated Emergent Reasoning System — is the canonical umbrella for this ecosystem. It replaces human-centered coordination and judgment with a governed, closed-loop, agentic process for solving complex problems. All components operate under this Constitution.

---

## 1) Authority Model
- **Umbrella (CERES):** decides coordination and reasoning semantics; sets invariants.
- **Governance/Orchestration:** enforces scope, staging, arbitration, and validation; cannot execute scope changes.
- **Execution/Runtime:** obeys approved tasks only; no authority over scope or routing.
- **Subsidiaries:** specs, UI constitutions, pattern registries, observability, security—all subordinate to CERES.

---

## 2) Lifecycle (governed flow)
1. **Objective Contract (draft → committed)** — goal, constraints, success criteria, allowed sources.
2. **Inference Phase** — readiness check; Gap Ledger creation; resolution strategy selection (ask/infer/prototype/assume with risk).
3. **Planning** — deterministic Task Plan; tasks materialized in `todo.md`; no execution before this exists.
4. **Controlled Prototyping** — explicitly tagged exploratory artifacts only to collapse uncertainty; cannot silently change scope.
5. **Lock-In Moment** — commit Objective + Plan; reject unconfirmed assumptions or elevate for approval.
6. **Execution (PDCA)** — task-by-task obedience; evidence captured; reopen gaps on failure.
7. **Verification** — tests/validation; updates to artifacts; audit trail in `completed.md`.

---

## 3) Interaction Protocol (attention-bounded)
- One decision/question per turn; tie each question to a Gap ID and rationale.
- Questions must be binary/bounded; provide example if free-form is required.
- Show compressed state before asking: decided, undecided, current gap, consequence.
- Progressive disclosure only; no multi-part or speculative sidebars.
- Explicit pause points after answers; no automatic cascades without policy.

---

## 4) Artifacts (authoritative)
- **Objective Contract:** goal, constraints, success criteria, allowed sources, risk profile.
- **Gap Ledger:** `gap_id`, type, blocking, answerable_by_system, resolution_method, confidence_required, status, evidence_links/assumptions (with risk + expiry).
- **Task Plan → `todo.md`:** sequenced tasks with concept/phase/acceptance; execution gate.
- **Audit → `completed.md`:** immutable log of completed tasks with evidence references.
- **Memory Ledger → `memory.md`:** canonical durable context; `handover.md` is an export snapshot for context transfer (if conflict, `memory.md` wins).
- **Prompt Debug Report:** YAML with prompt_id, status, detected_intent, scope, risk_level, issues, suggested_fix, decision_rationale; required for all intake before governance.
- **Assumptions:** explicit, time-bound, risk-rated; never silent.

---

## 5) Enforcement Rules (non-negotiable)
- No execution before Task Plan exists in `todo.md` and is stable/visible.
- Gap resolution requires evidence, user answer, or explicit assumption with risk/expiry.
- One-question-per-turn protocol enforced; non-compliant questions are rejected.
- Prompt Debugger gates all intake (file or chat) before governance; no silent auto-fixes.
- Preflight required: run `scripts/preflight.sh --mode execute` before any execution (Prompt Debugger + lifecycle gate).
- No cross-repo changes without explicit coordination.
- Execution cannot bypass observability/security; telemetry cannot be silenced.
- Push required before closing a task; record the push hash in `completed.md` (auto-push may be used when safe).
- No credentials in the repo; only placeholder values in env template files (e.g., `.env.example`).
- Same prompt → same decision; deterministic behavior over permissiveness.

---

## 6) Naming & Scope
- Umbrella name is **CERES — Coordinated Emergent Reasoning System** (canonical; no aliases above it).
- Subcomponents are CERES subcomponents; they must not redefine coordination or reasoning semantics independently.
- If a parent framework is proposed above CERES, reject; CERES is top-level.

---

## 7) Replacement Clause
- This Constitution supersedes any temporary bootstrap text.
- `PROMPTLOADER.md` must point here; if it diverges, this Constitution prevails.
- Updates to this Constitution must be explicit and versioned; no implicit drift.

---

## 8) Next Step Options
1. Update PROMPTLOADER.md to point here and remove temporary content.
2. Update sub-repo docs to reflect CERES naming and authority.
3. Implement Prompt Debugger and artifact schemas per this Constitution.
