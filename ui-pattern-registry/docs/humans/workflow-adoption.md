# Framework Adoption Guide

This guide explains how to apply the ai-agents-workflow framework in this repository to a new or existing project. It focuses on the minimum governance files, where to customize, and how to keep the framework auditable.

The framework is AI-operated: humans provide tasks/decisions via chat or `todo-inbox.md`, and the agent runs scripts plus updates AI-managed files.

## If you just want the fastest path
- Say: “Apply this ai agents framework to my new project at <path> using <stack> (with or without Skills).”
- Point to your stack profile under `docs/stacks/` (or the template).
- Let the agent run `scripts/bootstrap-workflow.sh` and then review the summary.

## 1. Pick the Stack Profile
- Choose the matching profile in `docs/stacks/` and follow it for layout, commands, linting, testing, and security expectations.
- If no profile matches, copy `docs/stacks/STACK.template.md`, customize it, and link it in `docs/wiki/index.md`.
- For multi-stack repos, document the primary stack per service or package and keep profiles scoped to the code they govern.

## 1.5 Quick Apply (One-Line Request)
If you want Codex to apply the framework for you, say exactly:

“Apply this ai agents framework to my new project at <path> using <stack> (with or without Skills).”

Codex execution checklist:
1) Confirm target path, stack profile, and whether Skills are included.
2) Run `scripts/bootstrap-workflow.sh [--with-skills] <target-dir>` to copy governance files.
3) Verify `skills/reasoning/` + `scripts/validate-reasoning-skills.py` exist in the target repo.
4) Update or add the stack profile (`docs/stacks/<stack>.md` from template if needed).
5) Run `scripts/create-workflow-revision.sh` and update the baseline line in `README.md`.
6) Record outcomes in `completed.md`, `handover.md`, and `CHANGELOG.md`, then commit and push.

## 2. Add the Core Governance Files
Minimum root-level files:
- `AGENTS.md` (authoritative rules)
- `todo-inbox.md` (user-managed intake)
- `todo.md`, `backlog.md`, `completed.md`, `handover.md`, `CHANGELOG.md` (agent-managed artifacts)
- `README.md` (framework revision baseline pointer)
- `.gitignore` (local artifacts and tooling ignores)

Minimum docs:
- `docs/agents.md` (operational framework)
- `docs/humans/` (human instruction docs: workflow-guide, workflow-adoption, user guide, cheat sheet)
- `docs/workflow-audit.md` (framework change audit log)
- `docs/context-management.md` (ledger and pruning protocol)
- `docs/security.md` and `docs/access-manifest.md` (security and access rules)
- `docs/wiki/index.md` and `docs/wiki/architecture-overview.md` (navigation only)
- `docs/wiki/playbooks/README.md` and `docs/wiki/playbooks/stack-quickstarts.md`
- `docs/stacks/<your-stack>.md`

Minimum Reasoning Skills artifacts:
- `skills/reasoning/` (Reasoning Skill manifests, schema, and pipeline)

Recommended support files (if you use the Skill system or snapshots):
- `skills/` (Skill packages), `skills/_template/`, `skills/_schema/skill.schema.json`
- `docs/skills/` and `specs/`
- `scripts/create-workflow-revision.sh` and `docs/workflow-revisions.md` (snapshots are stored locally under `ai_workflow_revisions/` and gitignored by default)
- `tests/` for deterministic tooling checks

## 3. Customize Project-Specific Details
- Replace org-specific references (for example, in `docs/agents.md`) with your team or company name.
- Align security expectations in `docs/security.md` and `docs/access-manifest.md` with your policies.
- Update stack profiles with the exact commands and tools your repo uses.
- Keep the wiki as navigation only; the authoritative rules live in `AGENTS.md` and the docs above.

## 4. Initialize Ledgers and Intake
- Create `docs/context/` and add at least `docs/context/planner-task-manager.md` using the template in `docs/context-management.md`.
- Keep `todo-inbox.md` in the provided four-section template so intake stays consistent.
- Ensure the agent-managed files (`todo.md`, `completed.md`, `handover.md`, `CHANGELOG.md`) start empty but present.

## 5. Establish Framework Revision Snapshots
- Keep `docs/workflow-revisions.md` up to date and have the agent run `scripts/create-workflow-revision.sh` after any governance change.
- Snapshots are stored locally under `ai_workflow_revisions/` and gitignored by default. If you choose to track them, update the baseline line in `README.md`.

## 6. Run the First Task
1. Create the first spec in `specs/` (or equivalent) and record its ID.
2. Add the work item to `todo-inbox.md` under the correct section.
3. Ask the agent to execute the workflow sequence: plan, implement, validate, and record outcomes in `completed.md`, `handover.md`, and `CHANGELOG.md`.

## 7. Operating Mode Defaults
- Continuous Mode is the default. It processes all runnable items and uses the Decision Queue (`Decision Needed: ...` entries under `## Decision Queue` in `todo.md`) for non-blocking decisions.
- Iterative Mode is explicitly enabled when you want the agent to pause at the first decision point; log that activation in the planner ledger and `handover.md`.

## 8. Clarification Gate
- Clarification Gate runs before planning when inputs are ambiguous or incomplete.
- Answers are recorded in the active spec under `Clarifications`, and the run restarts once updates are saved.

```markdown
Clarifications (optional):
- Q: Which cache backend should we use? A: Redis.
```

## 9. Reasoning Skills
- Reasoning Skills run after Clarification Gate and before planning using the ordered pipeline in `skills/reasoning/pipeline.yaml`.
- Manifests in `skills/reasoning/` are deterministic, non-executing constraints that can halt a run on violations.
- Structured logs should capture execution order, guarantees, violations, and abort reasons.
- Validate manifest changes with `scripts/validate-reasoning-skills.py`.

## Decision Queue Example
```markdown
# Todo

## Bugs

## Decision Queue
- Decision Needed: Confirm whether to use Redis or Postgres for caching.

## Workflow Governance

## Current Focus
- [ ] Implement cache interface for the session store.
```

## Adoption Checklist
- Stack profile chosen and documented.
- Governance docs present and customized.
- Ledgers and todo artifacts created.
- Snapshot tooling in place and baseline snapshot created.
- Team understands that wiki pages are navigation only.

If you are migrating an existing project, keep your existing build and test tooling, then update the stack profile to match reality rather than forcing the repo to match the template.

## Appendix A: Quick Copy List
Copy these items from the framework repo into the target project, then reset the files that should start empty.

Copy as-is:
- `AGENTS.md`
- `docs/agents.md`
- `docs/humans/`
- `docs/workflow-audit.md`
- `docs/context-management.md`
- `docs/security.md`
- `docs/access-manifest.md`
- `docs/wiki/index.md`
- `docs/wiki/architecture-overview.md`
- `docs/wiki/playbooks/`
- `docs/stacks/`
- `skills/reasoning/`

Copy, then reset contents:
- `todo.md` (empty sections)
- `backlog.md`
- `completed.md`
- `handover.md`
- `CHANGELOG.md`
- `todo-inbox.md` (keep the four-section template)
- `README.md` (merge the baseline snapshot note instead of replacing your README)
- `.gitignore` (merge entries; do not overwrite)

Generate fresh:
- `docs/context/planner-task-manager.md`
- `docs/context/archive/` (empty)
- `specs/` (empty directory for new specs)
- `ai_workflow_revisions/` (local snapshot folder; gitignored by default)

Optional (Skill system + snapshots):
- `scripts/create-workflow-revision.sh`
- `docs/workflow-revisions.md`
- `skills/`, `docs/skills/`, and `tests/` (only if adopting the Skill system)

## Appendix B: Bootstrap Script
The agent runs `scripts/bootstrap-workflow.sh` from this repo to scaffold a target project. It copies core governance files, seeds empty todo/ledger files, and skips existing files unless `--force` is provided. Add `--with-skills` to copy the Skill system scaffolding and tooling.
