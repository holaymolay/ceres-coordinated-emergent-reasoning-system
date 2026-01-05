Proceeding to **B: repo assignment**.
This is the **mechanical mapping** from layers → repos. No theory.

---

# B) Canonical Repo Assignment (Authoritative)

## 1️⃣ Umbrella Repo — **Ecosystem Coordinator**

**(new repo; entry point)**

**Owns / coordinates:**

* Layer 1 — Intent Intake
* Layer 4 — Task Materialization & Visibility
* Cross-cutting wiring between repos

**Responsibilities:**

* Human-facing entry point (CLI, chat, inbox)
* `task-inbox.md` lifecycle
* High-level orchestration
* Zero business logic
* Zero agent execution

**This repo answers:**

> “What is happening and why?”

---

## 2️⃣ Governance & Orchestration Repo

(**current `context-engineering-framework` → renamed governance/orchestrator**)

**Owns:**

* Layer 2 — Prompt Normalization & Enforcement
* Layer 3 — Pre-Execution Debugging & Validation
* Layer 5 — Planning, Parallelization & Arbitration

**Responsibilities:**

* Compiler front-end for intent
* Enforces invariants
* Breaks tasks into executable units
* Arbitration logic
* Rejects invalid work early

**This repo answers:**

> “Is this allowed, coherent, and correctly scoped?”

---

## 3️⃣ Execution / Agent Runtime Repo

(**Codex-facing runtime**)

**Owns:**

* Layer 6 — Execution (Agent Layer)

**Responsibilities:**

* Actual code generation
* PDCA loop execution
* Single-concept enforcement
* No authority over scope or routing

**This repo answers:**

> “Execute this exact, approved task.”

---

## 4️⃣ Observability & Telemetry Repo

(**can start embedded, but should extract**)

**Owns:**

* Layer 7 — Observability & Telemetry

**Responsibilities:**

* Metrics
* Logs
* Drift detection
* Cross-repo visibility

**Hard rule:**
Execution cannot silence this layer.

**This repo answers:**

> “What actually happened?”

---

## 5️⃣ Security & Access Repo

(**policy + enforcement artifacts**)

**Owns:**

* Layer 8 — Security & Access Enforcement

**Responsibilities:**

* Access manifest
* Least privilege definitions
* Abort rules
* Review gates

**Cross-cutting:** invoked by *every other repo*.

**This repo answers:**

> “Is this permitted at all?”

---

## 6️⃣ Spec Library Repo

(**immutable knowledge base**)

**Owns:**

* Layer 9 — Spec Library & Memory

**Responsibilities:**

* Spec authoring
* Spec reuse
* Immutable IDs
* Long-term durability

**Hard rule:**
No execution without a spec reference.

**This repo answers:**

> “What does ‘correct’ mean?”

---

# One critical invariant (do not violate)

**The umbrella repo coordinates.
The governance repo decides.
The execution repo obeys.**

If any repo both *decides* and *executes*, the system collapses.

---

## What’s left (small but real)

* Final naming of:

  * umbrella repo
  * governance repo
* Deciding whether Observability starts embedded or extracted
* Writing a **single diagram** that matches this mapping

If you want, next step we can:

* lock names, or
* produce the canonical diagram, or
* write the Codex bootstrap prompt that assumes this structure

Say which.
