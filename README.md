# CERES
**Coordinated Emergent Reasoning & Execution System**

---
## A Better Way to Build with AI
### How CERES Changes the Way AI Builds Projects

CERES is a system for **working with AI on projects in a clear, structured, and repeatable way**.

Many people build things with AI by describing what they want in plain language and adjusting as they go. That works at first, but as projects grow, problems appear:

- decisions get forgotten
- instructions drift over time
- the AI changes things you thought were settled
- progress becomes hard to track or repeat

CERES exists to solve that.

It gives the AI a **shared set of rules, memory, and structure** to operate within, so it doesn’t have to guess your intent every time.

Instead of relying on improvisation, CERES ensures that:
- ideas are turned into explicit decisions
- decisions are written down as artifacts
- the AI knows what phase of work it is in
- changes happen deliberately, not accidentally

You don’t manually “set up” CERES like software.

You open a project, and the AI **adopts CERES behind the scenes** by reading its instructions and using them as the operating rules for that project.

From that point on, the AI behaves less like an improviser and more like a disciplined collaborator that remembers what was decided, why it was decided, and what is allowed to change next.

CERES is for people who want AI to help build real projects that last — not just generate one-off results.
---

---
## Quick Start

CERES is bootstrapped and used through an AI coding agent.

To get started — including non-coder instructions using VS Code and Codex — follow the guided setup here:

➡️ **Start with:** `GETTING_STARTED.md`

That guide explains:
- how to prepare a project folder
- how the AI adopts CERES for that project
- how to recover if something stops working
---

---
## Documentation

CERES is documented as a set of small, authoritative files rather than a single manual.

To understand how the system works, how it is governed, and how to work within it, start here:

➡️ **Read the documentation index:** `DOCS.md`
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

## What this repo is

This repository is the **CERES coordination hub**:
- documentation and conventions
- schemas and artifacts
- lightweight scripts

CERES is designed as an ecosystem: this hub is the entrypoint, and additional components can live as independent repos with their own release cycles.

---

## Core components (high-level)

CERES is built to support independent components like:

- `governance-orchestrator` — governance/orchestration for coding agents  
- `readme-spec-engine` — spec-driven README generator/validator  
- `spec-compiler` — turns clarified intent into governed specs  
- `ui-constitution` — machine-readable UI constraints  
- `ui-pattern-registry` — approved UI patterns for LLM-driven front ends  

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
