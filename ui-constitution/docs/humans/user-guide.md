# AI Framework User Guide (Humans)

This guide explains how humans should plan, structure, and communicate work so the ai-agents-workflow framework produces fast, accurate results with minimal iteration. It complements `docs/humans/workflow-guide.md` (system overview) and `docs/humans/workflow-adoption.md` (setup).

## If you only have 2 minutes
- Read `docs/humans/user-guide-cheat-sheet.md`.
- Use the Request Pack below, keep one task at a time, and answer clarifications quickly.
- Add tasks in chat or `todo-inbox.md`; the agent handles scripts and AI-managed files.

## 1. What This Framework Is Good At
- Turning a clear, bounded request into working code quickly.
- Keeping changes auditable through specs, ledgers, and snapshots.
- Enforcing consistency via Skills, Concepts, and gated reasoning steps.

If you want speed + accuracy, your job is to supply a clean, bounded request with unambiguous success criteria.

## 2. Your Role (Human Responsibilities)
You provide:
- The goal and success criteria (what "done" means).
- Constraints (languages, frameworks, performance requirements, deadlines).
- Scope boundaries (what to touch, what to avoid).
- A minimal test plan or expected behavior examples.

The agent provides:
- Planning, implementation, and validation within the defined constraints.
- Documentation in `completed.md`, `handover.md`, and `CHANGELOG.md`.

The framework is AI-operated: use the chat window or `todo-inbox.md` to provide tasks and decisions. The agent runs scripts and updates AI-managed files; humans should not edit them manually.

## 3. Start With a Clean Request
Use this simple request pack so the agent can get it right on the first pass:

```markdown
Goal:
- What outcome do you want?

Context:
- Where should the change happen? (files, modules, areas)
- What must not change?

Constraints:
- Stack/framework/version requirements.
- Performance/security considerations.

Success criteria:
- Exact behavior that proves it works.
- Example input/output or user flows.

Testing:
- How should it be verified? (tests, commands, manual steps)
```

## 3.5 Quick Apply Phrase
If you want the framework applied to a new repo, say exactly:

“Apply this ai agents framework to my new project at <path> using <stack> (with or without Skills).”

## 4. Keep Scope Tight
Large, vague tasks lead to rework. If the change is big, split it into smaller steps:
- One feature or behavior per task.
- Avoid mixing refactors with new behavior in the same request.
- If you are unsure, ask for a plan before implementation.

## 5. Use the Spec Template (When Needed)
For significant changes, the agent will require a spec in `specs/`. You can help by pre-filling the template from `docs/agents.md`:
- Write the user story and functional requirements.
- Include your expected behavior and tests.
- State any dependencies explicitly.

## 6. Help the Clarification Gate
If the agent asks clarification questions, respond quickly with concrete answers. This reduces iteration and speeds delivery.

Examples of good clarifications:
- "Use PostgreSQL, not Redis."
- "Keep existing API responses unchanged."
- "Target Node 20 + Express 4."

## 7. Reasoning Skills and Constraints
Before planning begins, Reasoning Skills enforce guardrails (single Concept, single spec, no cross-concept work). To help:
- Provide the spec ID when possible.
- Confirm which Concept is in scope.
- Avoid asking for multi-concept changes in a single request.

## 8. Decision Queue vs. Blocking Decisions
- If a decision is blocking, the agent will stop and ask you.
- If a decision is non-blocking, it will be added to the Decision Queue for later.

You can speed delivery by pre-deciding important choices (APIs, data store, UI direction) and stating them upfront.

## 9. Operating Modes (Speed vs. Control)
- Continuous Mode (default) runs through all ready tasks and defers non-blocking decisions.
- Iterative Mode stops at the first decision point and waits for your input.

If speed is your priority, keep Continuous Mode and answer Decision Queue items in batches.

## 10. Tests and Verification
To minimize iteration:
- Give a clear test command or verification steps.
- Provide expected output or acceptance criteria.
- Avoid "just make it work" without defining what "work" means.

## 11. Anti-Patterns (Avoid These)
- Vague goals ("make it better").
- Mixed priorities ("refactor X and add Y and investigate Z").
- Missing constraints (stack/version, security needs, non-goals).
- Late-breaking requirements after work begins.

## 12. Speed + Accuracy Metrics
The framework tracks two metrics:
- Speed: time from request to working result.
- Accuracy: fix-loop count and first-pass success rate.

You help these metrics by providing clear requirements and fast clarifications.

## 13. Example: Strong vs Weak Request

Weak:
- "Fix the dashboard, it is slow and messy."

Strong:
- "Goal: Reduce dashboard load time to under 2 seconds.
  Context: Only update `src/dashboard/` and `services/metrics/`.
  Constraints: Keep existing API responses unchanged.
  Success: Load time <2s on cold start; no visual regressions.
  Testing: Run `npm test` and `npm run perf:dashboard`."

## 14. Where to Look
- Governance rules: `AGENTS.md`
- Operational details: `docs/agents.md`
- Framework overview: `docs/humans/workflow-guide.md`
- Adoption checklist: `docs/humans/workflow-adoption.md`
- Audit loop: `docs/workflow-audit.md`

Use this guide as a checklist before sending requests. Clear inputs lead to faster, more accurate outputs.
