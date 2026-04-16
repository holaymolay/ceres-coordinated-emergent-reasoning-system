# Glossary and quick definitions

This glossary gives newcomers clickable definitions for the framework’s most-used terms. It points to the authoritative sources so you can jump from a word to the governing document without guessing. Use it as a fast lookup while reading other docs.

## How to use this glossary
- Start here when a term in README or AGENTS is unfamiliar.
- Follow the provided links to the authoritative doc for deeper detail.
- If a term is missing, add it to `todo-inbox.md` so the glossary stays current.

## Core concepts
- **Context engineering**: Governance-first approach that turns requests into specs, Skills, and logged artifacts. See [AGENTS.md](../../AGENTS.md).
- **Spec**: Approved description of work stored under `specs/`; required before execution. See [docs/agents.md](../agents.md#3-specification-template-spec-driven-model).
- **Skill**: Deterministic tool package with `skill.yaml` and schemas under `skills/`. See [skills/README.md](../../skills/README.md).
- **Concept**: Domain-scoped contract that organizes specs and handlers. See [docs/wiki/architecture-overview.md](../wiki/architecture-overview.md).
- **Synchronization**: Cross-concept contract used when dependencies exist. See [synchronizations/](../../synchronizations/).

## Operating flow
- **Clarification Gate**: Pause to resolve ambiguity before planning. See [specs/clarification-gate-v1.md](../../specs/clarification-gate-v1.md).
- **Reasoning Skills pipeline**: Ordered pre-planner checks for guarantees and aborts. See [skills/reasoning/pipeline.yaml](../../skills/reasoning/pipeline.yaml).
- **PDCA loop**: Plan/Do/Check/Act cycle applied to every change. See [docs/agents.md](../agents.md#2-workflow-overview-pdca-integration).
- **Run record**: JSONL audit trail under `runs/YYYY-MM-DD/`. See [runs/run-record.schema.json](../../runs/run-record.schema.json) and [docs/execution-profiles.md](../execution-profiles.md).

## Governance artifacts
- **Handover**: Current state + next steps in [handover.md](../../handover.md).
- **Todos**: Agent-managed queue in [todo.md](../../todo.md); humans add items via [todo-inbox.md](../../todo-inbox.md).
- **README governance**: Spec-driven README enforced by CI; source of truth is `README_SPEC.yaml`. See [README_GOVERNANCE.md](../../README_GOVERNANCE.md).
- **Workflow revision**: Local snapshot under `ai_workflow_revisions/` captured after governance changes. See [docs/workflow-revisions.md](../workflow-revisions.md).

## UI intent protocol (UIP) terms
- **UI intent**: Structured object describing UI needs (no JSX/CSS). See [concepts/ui-intent-protocol/manifest.yaml](../../concepts/ui-intent-protocol/manifest.yaml).
- **Tailwind adapter**: Renderer that applies semantic tokens to intents. See [ui-adapters/tailwind/patterns/](../../ui-adapters/tailwind/patterns/).
- **UI governance Skill**: Validator that blocks markup/style leakage. See [skills/ui-governance/](../../skills/ui-governance/).
