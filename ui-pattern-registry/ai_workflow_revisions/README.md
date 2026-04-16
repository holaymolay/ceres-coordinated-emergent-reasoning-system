# Workflow Revision Snapshots

Workflow revisions are point-in-time snapshots of governance rules and supporting documentation. They exist so reviewers can diff policy changes over time.

## Naming Rules
- Revisions are stored under `ai_workflow_revisions/`.
- Folder names are sequential: `rev_001`, `rev_002`, …
- The latest baseline should carry the `_current` suffix: `rev_00N_current`.
- When creating a new baseline, rename the previous `_current` folder to remove the suffix.

Current baseline snapshot: `rev_001_current` (local, gitignored in this workspace). The next snapshot will increment to `rev_002_current`.

## Required Snapshot Contents
Copy the following into the revision folder, preserving relative paths:

Core governance:
1. `AGENTS.md`
2. `README.md`
3. `.gitignore`
4. `todo-inbox.md`
5. `todo.md`
6. `backlog.md`
7. `completed.md`
8. `handover.md`
9. `CHANGELOG.md`

Operational framework:
1. `docs/agents.md`
2. `docs/humans/`
3. `docs/workflow-audit.md`
4. `docs/context-management.md`
5. `docs/security.md`
6. `docs/access-manifest.md`
7. `docs/prompts/`
8. `docs/context/*.md`

Wiki navigation (non-authoritative summaries):
1. `docs/wiki/index.md`
2. `docs/wiki/architecture-overview.md`
3. `docs/wiki/playbooks/`

Stack profiles:
1. `docs/stacks/*.md`

Skill system scaffolding (not the full Skill library):
1. `skills/README.md`
2. `skills/_schema/`
3. `skills/_template/`
4. `skills/reasoning/`
5. `docs/skills/`
6. `specs/`

Tooling tests:
1. `tests/`

Snapshot tooling:
1. `scripts/`

## Create a New Snapshot
Use `scripts/create-workflow-revision.sh`. It:
- Finds the next `rev_00N_current` number
- Renames the prior `_current` folder (if present)
- Copies the required files/directories into the new revision folder

## Logging Requirements
- Record the new revision ID in `completed.md` and `handover.md`.
- Add a timestamped entry to `CHANGELOG.md`.
