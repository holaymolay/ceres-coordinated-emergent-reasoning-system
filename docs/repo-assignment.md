# Canonical Layer Assignment (Authoritative)

This is the mechanical mapping from layers to directories. All components live in a single monorepo.

## 1) Hub (repo root)

Owns / coordinates:
- Layer 1 — Intent Intake
- Layer 2 — Spec Elicitation (artifacts + prompts)
- Layer 4 — Task Materialization & Visibility
- Cross-cutting wiring between components

Responsibilities:
- Human-facing entry point (CLI, chat, inbox)
- `todo-inbox.md` lifecycle
- Governance contracts (`AGENTS.md`, `governance/inference-phases.yaml`)
- Synchronization contracts (`synchronizations/*.yaml`)
- Memory record schemas (`memory/records/*.json`)
- High-level orchestration
- Zero business logic
- Zero agent execution

This layer answers:
- What is happening and why?

---

## 2) Governance & Orchestration — `governance-orchestrator/`

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

This layer answers:
- Is this allowed, coherent, and correctly scoped?

---

## 3) Execution / Agent Runtime (embedded)

Owns:
- Layer 6 — Execution (Agent Layer)

Responsibilities:
- Actual code generation
- PDCA loop execution
- Single-concept enforcement
- No authority over scope or routing

This layer answers:
- Execute this exact, approved task.

---

## 4) Observability & Telemetry (embedded in hub)

Owns:
- Layer 8 — Observability & Telemetry

Responsibilities:
- Metrics
- Logs
- Drift detection
- Cross-component visibility

Hard rule:
- Execution cannot silence this layer

This layer answers:
- What actually happened?

---

## 5) Security & Access (embedded in hub)

Scope:
- Cross-cutting enforcement invoked by every layer

Responsibilities:
- Access manifest
- Least privilege definitions
- Abort rules
- Review gates

This layer answers:
- Is this permitted at all?

---

## 6) Spec Library (embedded in hub)

Owns:
- Layer 9 — Spec Library & Memory

Responsibilities:
- Spec authoring
- Spec reuse
- Immutable IDs
- Long-term durability

Hard rule:
- No execution without a spec reference

This layer answers:
- What does correct mean?

---

## Component directories

| Directory | Role |
|---|---|
| `governance-orchestrator/` | Governance & orchestration |
| `readme-spec-engine/` | Spec-driven README generator/validator |
| `spec-compiler/` | Intent-to-spec compiler pipeline |
| `ui-constitution/` | Machine-readable UI constraints |
| `ui-pattern-registry/` | Approved UI patterns for LLM-driven front ends |
| `parallel-agent-runner/` | Parallel agent execution runner |

---

## Critical invariant (do not violate)
- The hub coordinates.
- The governance layer decides.
- The execution layer obeys.

If any layer both decides and executes, the system collapses.
