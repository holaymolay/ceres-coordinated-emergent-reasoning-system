# Context-Engineering Framework for Coding Agents Guide

This document distills the Context-Engineering Framework for Coding Agents into a project-agnostic model for context-engineering teams. Use it whenever you need to port the governance model to another domain or explain the operating model to humans.

## If you need the short version
- Start with `HUMAN_START_HERE.md` and `docs/humans/user-guide-cheat-sheet.md`.
- Use `todo-inbox.md` for tasks/decisions and let the agent manage AI-owned files.
- Keep one Concept/task at a time; ask for a plan if the change is large.

## 1. Guiding Principles
- **Spec-first:** Every task is anchored to an approved spec (or equivalent source of truth) before implementation begins.
- **Single responsibility:** Each run focuses on one contained deliverable; handoffs and archives maintain continuity between runs.
- **Observable state:** Todos, handovers, and context ledgers capture the plan, execution notes, and outcomes so reviewers can audit after the fact. `handover.md` is the human-readable state transfer file; ask the agent to refresh it to reset the context window (especially when using models with smaller context limits).
- **Least necessary context:** Agents only keep the state they actively need. Everything else is pruned or archived with human approval.
- **AI-operated:** Humans provide tasks and decisions via chat or `todo-inbox.md`; the agent runs scripts and updates AI-managed files.

## 2. Roles & Artifacts
| Layer | Purpose | Core Artifacts |
| --- | --- | --- |
| Intake & Routing | Move requests from the inbox to the correct Concept/Skill | `todo-inbox.md`, `todo.md`, Concept manifests |
| Planning & Execution | Break work into substeps, run code/tests, and log evidence | Planner plan, shell/test logs, `completed.md` |
| Context Management | Keep per-agent ledgers minimal and auditable | `docs/context/<agent>.md`, `docs/context-management.md` |
| Governance & Knowledge | Capture policies and reusable playbooks | `AGENTS.md`, `docs/agents.md`, `docs/humans/workflow-guide.md`, wiki summaries |
| Revision Control | Snapshot framework governance rules whenever they change | `ai_workflow_revisions/` (local, gitignored) |

## 3. Flow Overview
1. **Capture** tasks in `todo-inbox.md`, grouped by Bugs → Decision Queue → Current Focus → Next Features → Backlog.
2. **Prioritize** framework-governance (workflow-change) requests above everything else, followed by Bugs and regular Current Focus items.
   - When multiple todos live inside the same priority block, list UI-focused entries before non-UI work so visual/experience regressions surface immediately.
3. **Clarify** ambiguous inputs or rules before planning.
   - Ask targeted questions, record answers in the active spec under `Clarifications`, and rerun the gate until resolved.
4. **Apply Reasoning Skills** to enforce deterministic constraints before planning.
   - Run the ordered pipeline and halt if violations are detected.
5. **Plan** the accepted work using the appropriate Concept manifest, spec, and Skill instructions.
   - If a single request requires more than two correction attempts, pause execution, restate your understanding to the user, and confirm next steps before coding again.
6. **Execute** inside the sanctioned sandbox, recording commands/tests.
7. **Validate** via lint/tests/security scans before presenting results.
8. **Document** outcomes (`completed.md`, `handover.md`) and archive governance docs if any governance files changed.

## 4. Operating Modes
- **Continuous Mode (default):** Work through all runnable items in `todo.md` in priority order and check off tasks as they complete.
  - **Decision Queue:** Deferred decisions recorded as `Decision Needed: ...` under `## Decision Queue` in `todo.md`.
  - If a decision blocks downstream work, stop and request user input.
  - If a decision is non-blocking, add it to the Decision Queue and continue. Resolve the Decision Queue after the continuous run finishes.
  - Still obey all governance rules, including pre/post `todo-inbox.md` sweeps between tasks, PDCA steps, and security constraints.
- **Iterative Mode (explicitly enabled):** Work through the current task queue and pause for user input as soon as a decision is required to proceed.
- **Continuous Execution Mode (phase-level override):** A scoped override that suppresses intermediate check-ins within a single phase/task. It can be used within either mode and only changes check-in cadence.

## 5. Clarification Gate
- Runs before planning (and before any Reasoning Skills, if enabled).
- Triggers when inputs are ambiguous, missing required context, or a reasoning check emits `needs_clarification`.
- Records answers in the active spec under `Clarifications`, then reruns the gate.
- No planning or execution occurs until clarifications are resolved.

## 6. Reasoning Skills
- Run the ordered pipeline in `skills/reasoning/pipeline.yaml` after Clarification Gate and before planning.
- Reasoning skills are deterministic, stateless, non-executing manifests under `skills/reasoning/`.
- Validate manifests against `skills/reasoning/reasoning-skill.schema.yaml` using `scripts/validate-reasoning-skills.py`.
- Emit structured logs for reasoning execution order, guarantees, violations, and abort reasons.
- Halt before planning if any reasoning failure condition is met.

## 7. Context & Pruning
- Each agent maintains a ledger under `docs/context/<agent>.md` with Active Entries, Pending Context Requests, and Archive Links.
- When switching Concepts or when ledgers grow beyond two task cycles, the Planner pings the Pruning Agent.
- The Pruning Agent summarizes the obsolete entries, seeks user approval, archives them under `docs/context/archive/`, and back-links the ledger.
- Declined prunes remain tagged as `Prune Deferred` to explain why context was retained.

## 8. Inter-Agent Communication
- Agents request information through ledger-based “Context Request” blocks rather than pulling whole files.
- Responses quote only the relevant snippet or explain why the request was declined.
- The Pruning Agent tracks outstanding requests to keep coordination tight without real-time chatter.

## 9. Framework Revision Snapshots
- Every change to framework governance (AGENTS, operational docs, this guide, wiki workflow pages, etc.) requires a snapshot.
- Copy the files listed in `docs/workflow-revisions.md` into the next sequential `rev_n` folder under `ai_workflow_revisions/` (gitignored by default).
- Reference the revision ID in the change log (`completed.md`) and `handover.md` so auditors can diff revisions quickly.

## 10. Adoption Checklist
1. Confirm the spec/Concept/Skill references exist.
2. Ensure todos/backlog/handovers reflect the new task.
3. Load only the ledger entries relevant to the current Concept.
4. Run code/tests within scope; no cross-concept jumps without a new plan.
5. Archive/prune as needed and produce the framework snapshot if governance docs moved.

## 11. Framework Audit Loop (Speed + Accuracy)
- For framework/governance changes, record a change proposal and outcome in `docs/workflow-audit.md`.
- Improvement Gate: answer the required question with the exact response before recommending or implementing a change.
- Measure speed (time-to-working result) and accuracy (first-pass success or fix-loop count) to keep iteration low.

This guide should travel with any deployment of the framework so other teams can reuse the same context-aware operating system with minimal adjustments.
