# Prompt: README + DOCS update

Prompt ID: ba8cf242-50f8-471f-8388-e8974557641f
Status: draft
Classification: atomic
Owner: user
Created: 2026-01-07T08:31:55.248365Z
Last-Modified: 2026-01-07T08:31:55.248365Z

## Intent
Update README.md and add DOCS.md exactly as specified, without touching code or schemas.

## Constraints
- Documentation-only changes.
- No code, scripts, schemas, enforcement logic, or UI assets.
- No new claims beyond existing functionality.

## Prompt Body
You are Codex operating inside the CERES repository workspace.

Your task is documentation-only.
Do NOT modify any code, scripts, schemas, enforcement logic, or UI assets.

You must update README.md and create a new DOCS.md file.
Do not invent features. Do not describe functionality that does not exist.

====================
OBJECTIVE
====================

1) Fix incorrect and misleading information in README.md.
2) Replace the current top-of-file explanation with the finalized, locked messaging.
3) Remove the incorrect “Try it in 60 seconds” UI instructions.
4) Consolidate documentation navigation into a single link.
5) Create DOCS.md as the canonical documentation index.

====================
PART 1 — UPDATE README.md
====================

Start from the EXISTING README.md in the repo and apply these changes carefully.

--------------------------------
A) TITLE
--------------------------------
Keep the main title, but update it to:

# CERES
**Coordinated Emergent Reasoning & Execution System**

Remove the tagline “Make AI finish what it starts.”

--------------------------------
B) REPLACE THE INTRODUCTION
--------------------------------
Replace everything from the top of the file down to (but NOT including) the first major section break
with EXACTLY the following content:

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

--------------------------------
C) REMOVE INCORRECT QUICK START
--------------------------------
Completely REMOVE the entire section:

## Try it in 60 seconds (no coding required)

Including:
- all references to a read-only UI
- all ZIP download instructions
- all references to opening ui/index.html

This section is incorrect and must not be replaced inline.

--------------------------------
D) ADD CORRECT QUICK START POINTER
--------------------------------
After the introduction section, add this section:

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

--------------------------------
E) CONSOLIDATE DOCUMENTATION NAVIGATION
--------------------------------
Remove ALL existing sections that enumerate or list documentation files, including but not limited to:
- “Developer quickstart”
- “Canonical references”
- Any multi-file navigation lists

Replace them with this single section, placed after Quick Start:

---
## Documentation

CERES is documented as a set of small, authoritative files rather than a single manual.

To understand how the system works, how it is governed, and how to work within it, start here:

➡️ **Read the documentation index:** `DOCS.md`
---

--------------------------------
F) PRESERVE HIGH-VALUE EXPLANATORY SECTIONS
--------------------------------
Keep (with minimal editing only if needed for consistency):
- “What CERES actually does (plain English)”
- “Why CERES is different”
- “What this repo is”
- Any conceptual explanations that do NOT contain installation steps

Remove low-level operational detail that belongs in docs (scripts, commands, platform notes).

====================
PART 2 — CREATE DOCS.md
====================

Create a new file at the repository root named DOCS.md.

DOCS.md is an index, not a tutorial.

Populate it with the following content structure:

---
# CERES Documentation Index

This page is the map of the CERES documentation.

Each document is small, authoritative, and intended to be read in context.

## Core concepts
- README.md — what CERES is
- CONSTITUTION.md — non-negotiable governance rules
- WHY_CERES.md — design rationale and motivation

## Getting started
- GETTING_STARTED.md — step-by-step setup (non-coder friendly)
- PROMPTLOADER.md — how AI agents adopt CERES

## Governance & lifecycle
- AGENTS.md — allowed agent behaviors
- PHASES.md — lifecycle ordering
- ENFORCEMENT.md — validation and gating rules

## Working with CERES
- TODO_SCHEMA.md — how work is represented
- SPEC_Elicitation.md — turning ideas into executable specs
- GAP_LEDGER.md — tracking unknowns and ambiguity

## System & architecture
- ARCHITECTURE.md — repository and artifact layout
- ANTI_PATTERNS.md — explicitly prohibited behaviors
- FAQ.md — common misunderstandings
---

Do not expand descriptions beyond one short line per document.

====================
OUTPUT REQUIREMENTS
====================

When finished:
- List the files modified or created
- Briefly summarize the change to each file

Do not ask questions.
Do not suggest additional improvements.
Execute exactly as specified.

