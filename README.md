# CERES Governance Orchestrator
Part of the CERES (Coordinated Emergent Reasoning System). Umbrella repo: [CERES](https://github.com/holaymolay/ceres-coordinated-emergent-reasoning-system).
**Hub alignment:** The authoritative entry for new projects is the CERES hub `PROMPTLOADER.md` + `CONSTITUTION.md`. Use the hub todo templates and init script (`scripts/init-todo-files.sh`) when bootstrapping; this repo stays independent and is pulled on demand via the hub clone/run scripts.



A governance and context-engineering framework that turns human requests into
repeatable, auditable agent execution.
It replaces ad-hoc prompting with explicit specs, Skills, and enforcement.
It captures context, decisions, and validation artifacts for reliable reuse.
It is designed for CLI- or IDE-driven coding agents.

## Who this is for
This framework is for engineers operating coding agents in production work.
It is for teams that need predictable outcomes and traceable decisions.

- Teams running agentic workflows in CLI or IDE environments.
- Engineers who require audit trails and deterministic behavior.
- Not for casual prompt experimentation or one-off scripting.

## Core problem
Agentic coding workflows fail when intent is ambiguous and outcomes drift.
They create clarification loops, non-deterministic edits, and no audit trail.
The result is fragile delivery that cannot be reliably reviewed or resumed.

## Solution (high level)
Context engineering turns intent into enforceable structure.
Specs define work, Skills constrain behavior, and governance records results.
The framework combines clarification gates, validation, and logged artifacts.

## What you get
- Deterministic execution boundaries for agent work.
- Auditable records of intent, decisions, and outcomes.
- Reduced human interruption through structured clarification.
- Portability across models and frontends via explicit contracts.

## How it works
Human intent flows through clarification, governed execution, and logging.
The framework records specs, plans, validations, and handover artifacts.

## Quick start
- Start here: [`HUMAN_START_HERE.md`](HUMAN_START_HERE.md) — human entrypoint.
- If you want the fastest path, read `docs/humans/user-guide-cheat-sheet.md` and paste the quick-start prompt there.
- Read `AGENTS.md` for the authoritative execution contract.
- Select a stack profile in `docs/stacks/`.
- Add tasks in chat or `todo-inbox.md`.
- Use `docs/humans/workflow-adoption.md` for new repositories.
- Use `docs/humans/glossary.md` when a term is unfamiliar.

## Repository map
- `AGENTS.md`: core governance rules and operating constraints.
- `docs/agents.md`: operational framework and execution flow.
- `docs/humans/`: human-facing guides and onboarding context.
- `docs/humans/glossary.md`: clickable definitions for framework terms.
- `docs/humans/concepts-map.md`: navigation map for common concepts.
- `docs/context/`: agent ledgers and context management protocol.
- `specs/`: spec contracts that govern changes.
- `skills/`: deterministic Skill packages and schemas.
- `docs/wiki/`: navigation layer for concepts and playbooks.
- `README_GOVERNANCE.md`: governs spec-driven README generation and enforcement boundaries.

## Design philosophy and non-goals
The framework optimizes for governance, determinism, and auditability.
It does not try to design UI, replace human judgment, or remove review.
It is not a prompt library or a set of agent heuristics.

## Context management as externalized state control

### Problem statement
- Conversational-only workflows drift: rules decay, specs get re-derived, and tokens bloat with repeated reminders.
- Implicit constraints vanish from the chat window, causing silent regressions.
- Context-window exhaustion forces premature truncation and re-teaching.

### Architectural shift
- Memory is externalized into versioned artifacts (`specs/`, `todo.md`, `completed.md`, `handover.md`, `runs/`).
- Narrative context becomes symbolic references (spec IDs, Concept manifests, Synchronizations).
- Control-plane chat is separated from state-plane repo artifacts (see `AGENTS.md` for authority boundaries).

### Mechanisms (concrete)
- `AGENTS.md` mandates spec-first execution and forbids free-form prompting.
- Specs and Concepts in `specs/` and `concepts/` encode requirements and handlers for reuse across sessions.
- Synchronization manifests in `synchronizations/` declare cross-concept coupling explicitly.
- PDCA and CI enforcement (`docs/agents.md`, `.github/workflows/`) validate lint, schema, and governance rules every run.
- Handover + run records (`handover.md`, `runs/`) rehydrate state without recalling prior chat.
- UI intent governance (`skills/ui-governance/`, `concepts/ui-intent-protocol/`) blocks markup/style leakage regardless of prior tokens.

### Why this reduces effective context pressure
- The model does not need to “remember” past instructions; it reloads specs, manifests, and run records on demand.
- Rehydration pulls authoritative files, not old messages, so truncation does not erase constraints.
- Lost chat tokens do not imply lost rules because enforcement lives in versioned artifacts and CI gates.

### Practical consequences
- Longer productive sessions without rule drift.
- Fewer correction loops because constraints are re-read, not re-taught.
- Easy session restarts: reload `handover.md`, `todo.md`, and relevant specs.
- Lower human cognitive load: follow the map instead of retyping context.
- The chat window stays lean; in typical runs it rarely exhausts context because state lives in files (limits still apply).
- Detailed rationale: see `docs/humans/context-management.md`.

### Non-claims and boundaries
- Does not increase raw token limits.
- Does not guarantee correctness without maintained specs and passing CI.
- Does not remove the need for human review or domain expertise.

## README Generation and Governance
README.md is produced from an explicit spec (`README_SPEC.yaml`) using the external `readme-spec-engine`.
This framework enforces README quality and structure but does not generate the README itself.
Generation happens outside this repo; enforcement here ensures the authored README stays aligned with its spec.