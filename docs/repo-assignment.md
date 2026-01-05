# Canonical Repo Assignment (Authoritative)

This is the mechanical mapping from layers to repos. No theory.

## 1) Umbrella Repo — Ecosystem Coordinator
**CERES hub (this repo)**

Owns / coordinates:
- Layer 1 — Intent Intake
- Layer 4 — Task Materialization & Visibility
- Cross-cutting wiring between repos

Responsibilities:
- Human-facing entry point (CLI, chat, inbox)
- `todo-inbox.md` lifecycle
- High-level orchestration
- Zero business logic
- Zero agent execution

This repo answers:
- What is happening and why?

---

## 2) Governance & Orchestration Repo
**governance-orchestrator**

Owns:
- Layer 2 — Prompt Normalization & Enforcement
- Layer 3 — Pre-Execution Debugging & Validation
- Layer 5 — Planning, Parallelization & Arbitration

Responsibilities:
- Compiler front-end for intent
- Enforces invariants
- Breaks tasks into executable units
- Arbitration logic
- Rejects invalid work early

This repo answers:
- Is this allowed, coherent, and correctly scoped?

---

## 3) Execution / Agent Runtime Repo
**Codex-facing runtime (model-specific)**

Owns:
- Layer 6 — Execution (Agent Layer)

Responsibilities:
- Actual code generation
- PDCA loop execution
- Single-concept enforcement
- No authority over scope or routing

This repo answers:
- Execute this exact, approved task.

---

## 4) Observability & Telemetry Repo
**Embedded for now; extract later**

Owns:
- Layer 7 — Observability & Telemetry

Responsibilities:
- Metrics
- Logs
- Drift detection
- Cross-repo visibility

Hard rule:
- Execution cannot silence this layer

This repo answers:
- What actually happened?

---

## 5) Security & Access Repo
**Policy + enforcement artifacts**

Owns:
- Layer 8 — Security & Access Enforcement

Responsibilities:
- Access manifest
- Least privilege definitions
- Abort rules
- Review gates

Cross-cutting:
- Invoked by every other repo

This repo answers:
- Is this permitted at all?

---

## 6) Spec Library Repo
**Immutable knowledge base**

Owns:
- Layer 9 — Spec Library & Memory

Responsibilities:
- Spec authoring
- Spec reuse
- Immutable IDs
- Long-term durability

Hard rule:
- No execution without a spec reference

This repo answers:
- What does correct mean?

---

## Critical invariant (do not violate)
- The umbrella repo coordinates.
- The governance repo decides.
- The execution repo obeys.

If any repo both decides and executes, the system collapses.
