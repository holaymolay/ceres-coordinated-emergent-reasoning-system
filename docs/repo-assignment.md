# Canonical Repo Assignment (Authoritative)

This is the mechanical mapping from layers to repos. No theory.
Status note: Conceptual repos are explicitly marked as embedded until extracted.

## 1) Umbrella Repo — Ecosystem Coordinator
**CERES hub (this repo)**

Owns / coordinates:
- Layer 1 — Intent Intake
- Layer 2 — Spec Elicitation (artifacts + prompts)
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
- Layer 3 — Inference & Gap Analysis
- Layer 4 — Planning / Decomposition (logic)
- Layer 5 — Governance & Arbitration

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
Status: Embedded for now (execution occurs via external runtimes; no standalone repo yet).

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
Status: Embedded for now (hooks live in hub; extract once schemas stabilize).

Owns:
- Layer 8 — Observability & Telemetry

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
Status: Embedded for now (policy artifacts remain in hub until enforcement exists).

Scope:
- Cross-cutting enforcement invoked by every layer

Responsibilities:
- Access manifest
- Least privilege definitions
- Abort rules
- Review gates

This repo answers:
- Is this permitted at all?

---

## 6) Spec Library Repo
**Immutable knowledge base**
Status: Embedded for now (specs live across hub/components; extract after canonical catalog exists).

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
