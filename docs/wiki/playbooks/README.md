# Playbooks

Procedural workflows for humans and agents. Each playbook references the authoritative manifests/specs/Skills—follow those files for exact schemas.

## Skill Reference
- **Skill Library v1** — Deterministic, LLM-agnostic Skill system design (`docs/skills/skill-library-v1.md`), contract schema (`skills/_schema/skill.schema.json`), and scaffolding (`skills/_template/`).

## Framework Adoption
- **Framework Adoption Guide** — Authoritative onboarding checklist for applying the framework to a new project (`docs/humans/workflow-adoption.md`).

## User Guide
- **User Guide** — Human-facing instructions for planning and structuring requests to maximize speed and accuracy (`docs/humans/user-guide.md`).
- **User Guide Cheat Sheet** — One-page quickstart for rapid, accurate requests (`docs/humans/user-guide-cheat-sheet.md`).
  - Quick apply phrase: “Apply this ai agents framework to my new project at <path> using <stack> (with or without Skills).”

## Framework Audit
- **Framework Audit Log** — Evidence log for framework changes (speed + accuracy), including the Improvement Gate and audit templates (`docs/workflow-audit.md`).

## Decision Queue
- **Decision Queue** — Use the `## Decision Queue` section in `todo.md` and `todo-inbox.md` for non-blocking decisions discovered during Continuous Mode; log items as `Decision Needed: ...` and resolve after the continuous run finishes.

## Clarification Gate
- **Clarification Gate** — Pre-planner questions to resolve ambiguous specs; record answers under `Clarifications` in the active spec and rerun before planning.

## Reasoning Skills
- **Reasoning Skills** — Pre-planner deterministic constraints executed via `skills/reasoning/pipeline.yaml`; manifests live in `skills/reasoning/` and emit structured logs.
- **Checklist**: Run `scripts/validate-reasoning-skills.py` after edits; log `event_type`, `skill_name`, `order`, `guarantees`, `violations`, `abort_reason`; abort before planning on any violation.

## Stack Quickstarts
- **Stack Quickstarts** — Fast guide to select and apply stack profiles (`docs/wiki/playbooks/stack-quickstarts.md`).

## UI Intent Protocol
- **UI Intent Protocol** — How to emit validated UI intent objects and render via the adapter (`docs/wiki/playbooks/ui-intent-protocol.md`).

## Create a New Concept
1. Review `todo-inbox.md`/`todo.md` for the scoped request and confirm a spec exists in `/specs/`.
2. Copy `/templates/concept-template.yaml` into `concepts/<name>/manifest.yaml` and fill in purpose, handlers, dependencies, and Synchronizations.
3. Scaffold `concepts/<name>/handlers` + `concepts/<name>/tests`, wiring only the code declared in the manifest.
4. Update `handover.md`, `todo.md`, and `docs/wiki/patterns.md` if the new Concept introduces reusable patterns.

## Create a New Synchronization
1. Confirm at least two Concepts need to collaborate and gather the governing specs/Skills.
2. Create `/synchronizations/<name>.yaml` using the existing sync schema (participants, trigger, actions, constraints).
3. Route the contract through the Arbitration + Security Agents for approval before touching code.
4. Reference the sync in affected Concept manifests and any dependent Skills.

## Create a New Skill
1. Validate that a spec exists and no current Skill covers the workflow (search `/skills/` + `docs/wiki/index.md`).
2. Copy `/skills/_template/` into `/skills/<skill-slug>/` and update `skill.yaml`, schemas, implementation, and tests.
3. Update `todo.md`/`backlog.md` entries with the `Skill: <name>` prefix and log the addition in `handover.md` + `docs/wiki/design-decisions.md` if architectural.
4. Notify the Security Agent if the Skill touches restricted data or credentials and update `docs/access-manifest.md` as needed.

## Update the Wiki
1. Make the authoritative change first (spec, manifest, Skill, etc.).
2. Identify which wiki pages summarize that content (index, architecture overview, patterns, design decisions, playbooks) and update only the relevant sections.
3. Cite the authoritative file(s) you updated so future readers know where to find the source of truth.
4. Mention the wiki update in `handover.md` if it accompanies a notable architectural or pattern change.

## Prune Agent Context
1. Check `docs/context/` for ledgers tied to the agents involved in the current work.
2. If the task switches Concepts/features or ledgers exceed two task cycles, draft a prune summary (agent, Concept, entry count, rationale).
3. Ask the user for approval, referencing the summary and proposed archive location under `docs/context/archive/`.
4. Upon approval, move the entries into the archive file, add a backlink inside the live ledger, and log the action in `completed.md` + `handover.md`.
5. If approval is denied, annotate the ledger with `Prune Deferred` and keep the entries in place until conditions change.

For a broader overview of how these playbooks fit together, share `docs/humans/workflow-guide.md` with stakeholders who need the high-level framework narrative (including the workflow sequence), and use `scripts/create-workflow-revision.sh` whenever governance docs change so the local `ai_workflow_revisions/rev_n/` snapshots stay consistent (gitignored by default).
