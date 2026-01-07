# CERES — Coordinated Emergent Reasoning System

**Make AI finish what it starts.**

CERES is a framework that helps you use AI on **long, complex work** (like building software or solving multi-step problems) without the usual breakdowns:

- the AI **forgets earlier decisions**
- progress **dies when the chat gets long**
- the AI gets stuck in a **fix → break → fix** loop
- you end up **starting over** in a new window

CERES fixes that by turning “a chat” into a **structured workflow** with:
- written-down decisions (so nothing important gets lost),
- guardrails (so the AI doesn’t thrash),
- and validation (so progress is real, not vibes).

### The big benefits
- **Stay in one thread:** durable artifacts reduce “context window collapse.”
- **No debug-death-spiral:** constrained, checkable steps prevent chaos.
- **More trust, less luck:** plans + decisions are visible and repeatable.
- **Extend safely:** add capabilities without giving the AI unlimited freedom.

---

## Try it in 60 seconds (no coding required)

CERES includes a **read-only UI** that shows what the system is doing.

1. GitHub → **Code** → **Download ZIP**
2. Unzip it
3. Open: `ui/index.html`

The UI is intentionally **read-only**:
- it **only reads artifacts**
- it does **not** mutate your project
- it degrades gracefully when artifacts are missing

---

## Who CERES is for

### If you don’t code
You can still benefit because CERES is about **keeping AI organized**:
- it captures what the AI decided
- it shows what the plan is
- it shows what changed and why
- it prevents “we’re lost again” moments

You get a clearer, safer AI workflow—even if you don’t write the code yourself.

### If you build software
CERES is for you if you’re tired of:
- “the AI rewrote half the project”
- “it contradicted its own earlier plan”
- “it fixed the bug but broke everything else”
- “I can’t reproduce the result twice”

CERES forces:
- explicit plans before execution
- bounded changes
- deterministic ordering
- validations before progress is accepted

### If you’re a founder/team
CERES is for you if you need:
- repeatable delivery (not prompt-lottery)
- traceability (“why did we do this?”)
- predictable workflows that multiple people can follow
- guardrails that prevent silent regressions

---

## What CERES actually does (plain English)

CERES treats ambiguity as a failure mode.

Instead of letting an AI “guess and go,” CERES forces a closed-loop process:

1. **Clarify**
   - identify missing info and contradictions early

2. **Plan**
   - convert intent into a task plan (written down)

3. **Validate**
   - reject plans that violate constraints or hide dependencies

4. **Decide**
   - pick a deterministic execution order (no randomness)

5. **Execute**
   - make small, scoped changes (not sweeping rewrites)

6. **Log**
   - record what happened so you can resume, audit, and debug reliably

This structure is why CERES is good at long projects where normal AI usage breaks down.

---

## Developer quickstart (optional)

<details>
<summary><strong>Show developer setup</strong></summary>

### Start here
1. Read `PROMPTLOADER.md` (bootstrapping CERES)
2. Read `CONSTITUTION.md` (ordering + governance rules)

### Initialize artifacts
- `scripts/init-artifacts.sh`
- `scripts/init-todo-files.sh`

### Run preflight gates
- Plan mode: `scripts/preflight.sh --mode plan`
- Execute mode: `scripts/preflight.sh --mode execute`

### Platform notes
- macOS/Linux supported natively
- Windows: use WSL (Ubuntu recommended)

</details>

---

## Preflight lifecycle (governance gates)

Preflight runs a fixed sequence of checks before any planning or execution:

1. **Spec elicitation gate**  
   Requires `ready_for_planning: true` and an empty `blocking_unknowns` list in the elicitation record.
2. **Governance contract validation**  
   Confirms the active **phase**, **agent**, and **pattern** are allowed by the governance registry.
3. **Lifecycle gate**  
   Validates the task plan, gap ledger, and prompt report requirements.

### What “ready_for_planning” means

`ready_for_planning: true` is the explicit signal that elicitation is complete and ambiguity has been resolved enough to proceed. If it is `false` or `blocking_unknowns` is non-empty, preflight stops immediately.

### Failure semantics

- **Early aborts** emit a `gate:fail` event before exiting (e.g., missing artifacts or non-ready elicitation).
- **Lifecycle violations** emit `gate:fail` from the lifecycle enforcement step.

### Observability guarantees

- Every enforced stop emits a structured event.
- Events include **phase**, **agent**, and **pattern** when known.
- Spec identifiers are included when available; early failures may omit them if a real spec does not exist yet.

---

## What this repo is

This repository is the **CERES coordination hub**:
- documentation and conventions
- schemas and artifacts
- lightweight scripts
- a read-only UI for visibility

CERES is designed as an ecosystem: this hub is the entrypoint, and additional components can live as independent repos with their own release cycles.

---

## Core components (high-level)

CERES is built to support independent components like:

- `governance-orchestrator` — governance/orchestration for coding agents  
- `readme-spec-engine` — spec-driven README generator/validator  
- `spec-compiler` — turns clarified intent into governed specs  
- `ui-constitution` — machine-readable UI constraints  
- `ui-pattern-registry` — approved UI patterns for LLM-driven front ends  

(See `docs/repo-assignment.md` and `docs/routing.md` for how components are mapped.)

---

## Why CERES is different

Many “agent frameworks” try to win by adding:
- more tools
- more agents
- more autonomy

CERES wins by adding:
- **constraints**
- **determinism**
- **validation**
- **auditability**
- **bounded extensibility**

In short:
> CERES is an operating system for reliable AI work.

---

## Python fallbacks (portability without risk)

CERES uses a conservative portability strategy:
- shell scripts remain authoritative unless explicitly promoted
- Python mirrors exist as fallbacks
- promotion to Python-primary only happens after parity verification and hardening

---

## Canonical references

- `docs/canonical-layer-model.md`
- `docs/repo-assignment.md`

---

## If you want to help / talk about CERES

The most valuable contributions are real-world failure modes like:
- “the AI forgot X and everything derailed”
- “it got stuck in a debug loop”
- “it changed too much at once”
- “I couldn’t resume the work later”

Open an issue with:
- what you tried to do
- where the AI drifted
- what you wish CERES had enforced earlier

Goal:
**turn AI from a clever improviser into a reliable collaborator.**
