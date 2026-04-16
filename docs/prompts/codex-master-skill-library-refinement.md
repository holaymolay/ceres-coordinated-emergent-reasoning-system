# Codex Master Prompt — Skill Library Refinement & Repository Design

Use this prompt to start a Codex session focused on refining the Skill Library as deterministic, LLM-agnostic capability infrastructure.

Note: In this repository, the authoritative v1 Skill system spec is `specs/skill-library-v1.md` (see also `docs/skills/skill-library-v1.md`).

---

Below is the prompt template (verbatim):

---

## CODEX MASTER PROMPT — Skill Library Refinement & Repository Design

**Role**
You are Codex, operating inside this Codex agent framework.
AGENTS.md is the single source of truth. You must not violate it.

Your task is to **extend and refine the framework with a first-class, LLM-agnostic Skill system**, without introducing agents, planners, memory, or prompt-embedded logic.

---

## Objective

Design and propose a **comprehensive, reusable Skill Library repository** that:

* Is deterministic and testable
* Is executable without any LLM
* Is callable by Codex, GPT-class, Claude-class, MCP, or CLI tools
* Cleanly integrates with:

  * Concepts
  * Synchronizations
  * PDCA
  * Security & Access governance
* Preserves portability and avoids vendor lock-in

You are **not** building agents.
You are **not** adding reasoning.
You are building **capability infrastructure**.

---

## Hard Constraints (Non-Negotiable)

You must enforce all of the following:

1. **Skill Definition**

   * Stateless
   * Deterministic
   * Schema-defined IO
   * Executable without an LLM
   * Testable in isolation

2. **Separation of Concerns**

   * LLMs select and parameterize skills
   * Agents orchestrate
   * Skills execute
   * No prompts inside implementations
   * No memory, planning, or questioning inside skills

3. **Framework Compatibility**

   * Must align with:

     * AGENTS.md
     * Concept–Synchronization architecture
     * PDCA loop
     * Security Guidelines
     * Access Manifest

4. **Governance**

   * Every skill references a Spec ID
   * One skill per commit
   * No external calls without Security Agent approval
   * Skills are shared infrastructure, not concept logic

---

## Primary Deliverables

You must produce **design artifacts**, not code dumps, unless explicitly requested.

### 1. Skill Repository Architecture

Propose a canonical repository layout, including:

* Directory structure
* Naming conventions
* Versioning strategy
* Language support policy (TS / Python / Shell)
* Test execution model (CI-friendly)

### 2. Canonical Skill Contract (Finalized)

Refine and finalize the portable `skill.yaml` contract.

You must:

* Justify each required field
* Define allowed extensions
* Specify schema validation rules
* Show how this contract maps to:

  * Codex
  * MCP tools
  * CLI execution

### 3. Codex Skill Conversion Protocol

Formalize the **mandatory Codex prompt** used to convert upstream skills into normalized skills.

Output it as a **locked template**.

### 4. Upstream Skill Ingestion Policy

For each source class below, define:

* What is allowed
* What is rejected
* Required transformation steps

Sources:

* OpenAI Codex Skills
* Anthropic Skills
* Microsoft Semantic Kernel
* LangChain tools
* MCP servers

### 5. Foundational Skill Taxonomy (v1)

Produce a **prioritized skill taxonomy** suitable for bootstrapping the system.

Rules:

* Atomic
* Cross-domain
* No business logic
* No organization-specific logic

### 6. Integration Points with Existing Framework

Explicitly map how Skills interact with:

* Concepts
* Synchronizations
* Planner / Task Manager
* Security Agent
* Observability Agent
* Caching Agent

---

## What NOT to Do

You must not:

* Introduce a new agent type
* Add planning logic to skills
* Use prompt-based implementations
* Redesign AGENTS.md
* Assume a specific LLM vendor
* Hide logic in markdown prose

---

## Output Format

Produce output in the following order:

1. **Executive Summary (≤ 10 bullets)**
2. **Skill Repository Architecture**
3. **Canonical Skill Contract**
4. **Codex Skill Conversion Prompt (Final)**
5. **Upstream Ingestion Policy**
6. **Foundational Skill Taxonomy**
7. **Framework Integration Map**
8. **Open Risks & Mitigations**

Be precise.
Be enforceable.
Assume this will be used as a long-lived system spec.

---

## Success Criteria

Your response is correct if:

* Another Codex instance could build the Skill Library without ambiguity
* Skills remain executable without any LLM present
* Agents become simpler, not smarter
* Vendor lock-in is structurally impossible
* Security and observability improve, not degrade

AGENTS.md is law.
Skills are infrastructure.
Proceed.
