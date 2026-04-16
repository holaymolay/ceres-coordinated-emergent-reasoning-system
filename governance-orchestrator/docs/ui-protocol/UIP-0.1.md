# UIP-0.1 — Intent-Driven UI Protocol

**Status:** Frozen (v0.1)
**Scope:** Agent ↔ UI boundary only
**Non-goal:** Rendering, styling, UX taste, or frontend frameworks

---

## 1. Purpose

UIP-0.1 defines a **renderer-agnostic protocol** for:

* Declaring user-interface intent
* Rendering that intent via compliant adapters
* Emitting structured UI events
* Routing events into domain Concepts via Synchronizations

UIP-0.1 exists to **eliminate UI hallucination**, **enforce determinism**, and **separate intent from presentation**.

---

## 2. Protocol Boundary (Hard Line)

UIP-0.1 governs **only** the shaded region below:

```
[ Agent / Skill ]
        │
        │  emits UIIntent (protocol artifact)
        ▼
===========================
      UIP-0.1
===========================
        │
        │  Adapter renders intent
        ▼
[ Renderer (React, CLI, etc.) ]
        │
        │  emits UIEvent (protocol artifact)
        ▼
[ Synchronizations → Concepts ]
```

Anything **above** UIP-0.1 is **logic**.
Anything **below** UIP-0.1 is **presentation**.

They MUST NOT leak into each other.

---

## 3. Core Protocol Artifacts (Frozen)

UIP-0.1 defines exactly **two first-class artifacts**.

### 3.1 UIIntent

A **UIIntent** is a declarative description of *what interaction is required*, not how it looks.

**Properties (required):**

* `id`
* `type`
* `purpose`
* `payload`
* `schemaVersion`

**Rules:**

* JSON-serializable
* Deterministic
* Renderer-agnostic
* No JSX, HTML, CSS, Tailwind, layout hints, or visual language

**Ownership:**

* Emitted only by the `ui.intent.emit` Skill
* Never modified by renderers

---

### 3.2 UIEvent

A **UIEvent** is a structured record of *what the user did*.

**Properties (required):**

* `id`
* `ts`
* `uiSessionId`
* `intentId`
* `type`
* `payload`
* `idempotencyKey`
* `schemaVersion`

**Rules:**

* Emitted only by adapters
* Never mutates domain state directly
* Routed via Synchronizations
* Fully auditable and replayable

---

## 4. Compliance Requirements

### 4.1 Agent / Skill Compliance

Agents:

* MUST NOT output JSX, HTML, CSS, or Tailwind
* MUST emit UIIntent **only via Skill invocation**
* MUST treat UI as infrastructure, not content

Violation = protocol breach.

---

### 4.2 Adapter Compliance

Adapters:

* MUST accept only validated UIIntent objects
* MUST render via patterns + tokens
* MUST emit UIEvent objects on interaction
* MUST NOT contain business logic

Adapters are **pure translators**.

---

### 4.3 Renderer Compliance

Renderers:

* MAY vary freely (React, CLI, mobile)
* MUST NOT alter intent semantics
* MUST NOT inject domain behavior

Renderers are replaceable.

---

## 5. Synchronization Contract (Mandatory)

All UIEvents MUST flow through a Synchronization.

Rules:

* UIEvent → Concept input mapping must be explicit
* Concepts own all state changes
* Idempotency is REQUIRED
* Authorization scope MUST be declared

No direct UI → domain writes are permitted.

---

## 6. PDCA Governance

UIP-0.1 allows evolution **only through PDCA**.

### Allowed changes

* Intent schema extensions
* Token adjustments
* Pattern library additions
* Adapter optimizations

### Forbidden changes

* Agent-side rendering
* Visual opinion injection
* Breaking schema without version bump
* Bypassing Skills or Synchronizations

---

## 7. Versioning Rules

* `schemaVersion` is REQUIRED on all protocol artifacts
* Minor version = additive, backward compatible
* Major version = breaking, requires explicit migration

UIP-0.1 is **intentionally minimal**.

---

## 8. Non-Goals (Explicit)

UIP-0.1 does NOT define:

* Colors
* Typography
* Spacing values
* Animations
* Layout pixels
* UX heuristics

Those belong to adapters and pattern libraries.

---

## 9. One-Line Invariant (Enforcement Test)

> Any compliant agent can emit UIIntent without knowing the renderer,
> and any compliant renderer can render UIIntent without knowing the agent.

If this stops being true, UIP has been violated.

---

## 10. Lock Statement

UIP-0.1 is **frozen**.

All future work MUST:

* Reference this document
* Declare compliance
* Justify deviations explicitly

---
