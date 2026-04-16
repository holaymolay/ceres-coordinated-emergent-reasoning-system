# Handover

**AI-managed file — humans should not edit this directly.** The agent keeps current state and next steps here.

## Current Focus
- Workflow governance: add a dedicated Housekeeping section to `todo-inbox.md`.
- Workflow governance: rename `ai_workflow_revisions` to `framework_revisions` for clarity.
- Bug backlog: default canonical branch choice should prefer `master` when prompted between `main` and `master` (captured in `todo.md`).

## State Snapshot
- Todo lists are updated: `todo-inbox.md` is cleared; `todo.md` now tracks the branch-name bug and two workflow-governance items (housekeeping section + revision directory rename); Current Focus and Backlog are empty.
- Post-task push enforcement tightened: `scripts/verify-sync.sh` blocks dirty/misaligned branches, run receipts require `push_hash`, and `scripts/git-hooks/post-commit-push-check.sh` provides an advisory warning. Governance docs (AGENTS + docs/agents) and the workflow audit log reflect the new checklist.
- Latest pushes on origin/master: 65e50bcd6bcf4561fc354dc43681f1c008a58426 (metadata), ad3629b1f311d359f61597cb4c401d7ac8dbab83 (run receipt/logging), bbe2caf0aa811238ccc27de2a247358fdd2c0382 (push housekeeping), 52a104902f4e297fd3580fa1f407ef34061e1606 (logging/run-receipt), bccaacaa41a803e672e8f48c0c21c85226abf3c8 (push enforcement). Run receipts: `runs/2025-12-28/4192e8f4-baf3-4224-b0e2-6e55e855f5fc.jsonl`, `runs/2025-12-28/7e772c91-05d7-4857-bb82-f1725a740260.jsonl`.
- Design Intent Schema concept lives in `concepts/design-intent-schema/` with the JSON Schema in `schemas/design-intent.schema.json` and a fail-fast validator in `handlers/intent/validate.py`.
- README governance docs now declare spec-driven generation, and `README_GOVERNANCE.md` is present.
- Workflow snapshots are stored locally under `ai_workflow_revisions/`; `rev_010_current` captures the push-enforcement updates (see `docs/workflow-revisions.md`).
- Clarifying docs for newcomers live in `docs/humans/glossary.md` and `docs/humans/concepts-map.md`, linked from README, HUMAN_START_HERE, and the wiki index.
- Context management deep dive is in `docs/humans/context-management.md`, linked from README and the wiki index.
- README quick start now highlights `HUMAN_START_HERE.md` as the first entrypoint.
- Spec compiler enforcement CI (`spec-compiler-enforcement` workflow) requires spec-generation-framework provenance, validation, Codex prompt checks, and compiler-version drift detection.
- Context management doc now follows a structured, falsifiable outline for why the framework reduces context pressure and supports resumable workflows.
- README quick start now includes a plain-English note that the chat window stays lean because state is externalized (limits still apply).
- README and human guides now include beginner-friendly entry points; cheat sheet links are surfaced for fast onboarding.
- UI intent protocol concept is under `concepts/ui-intent-protocol/` with schema, adapter, reference renderer, and PDCA doc; Skill `skills/ui-intent-emit/` added for validated intent emission.
- Key references: `AGENTS.md`, `docs/agents.md`, `docs/humans/workflow-guide.md`, `docs/context-management.md`, `docs/security.md`, `docs/access-manifest.md`, `docs/skills/skill-library-v1.md`, `specs/skill-library-v1.md`, `scripts/skillctl`, and `skills/README.md`.
- Upstream metadata catalog for agent selection: `docs/skills/upstream-skillcards.anthropic.json`.
- `skillctl` setup script creates `.venv-skillctl/` (ignored by git via `.gitignore`).
- Stack profiles live under `docs/stacks/` (Node, Python, Go, React/TS, Java/Spring, Rust, Data/ML, .NET, PHP, Mobile, Next.js, SvelteKit, Vue/Nuxt, React Native, Flutter, Electron/Tauri, R, PySpark, Julia, Rails, Django/DRF, FastAPI, serverless variants, C/C++, Elixir, Kotlin, Scala, Terraform, Ansible, Angular, Remix, Cloudflare Workers, Deno/Fresh, Unity, WordPress).
- AgentFS enforcement artifacts live under `docs/agentfs/` with the governing spec in `specs/agentfs-enforcement-layer-v1.md`.

## Active Skills and Recent Changes
- Skill scaffolding exists under `skills/_template/` and the contract schema is `skills/_schema/skill.schema.json`; implemented Skills: `skills/fs-hash-tree/`, `skills/skillcard-parse/`, and `skills/skillcard-index/`.
- Added Skill `ui_intent.emit` under `skills/ui-intent-emit/` for UI intent validation (Spec ID: `d520edbb-18e7-4b29-834c-6756329b2c81`).
- Added Skill `ui_governance` under `skills/ui-governance/` for UI governance constraints and capability gating.

## Recent Progress
- Pushed housekeeping changes to origin/master and logged run receipt `runs/2025-12-28/4192e8f4-baf3-4224-b0e2-6e55e855f5fc.jsonl`. Push hash: 65e50bcd6bcf4561fc354dc43681f1c008a58426 (work commit bbe2caf0aa811238ccc27de2a247358fdd2c0382). Skill: none. (ledger: 2025-12-28T19:26:40-08:00 — Git push housekeeping).
- Hardened post-task push enforcement (verify-sync guard, `push_hash` receipts, advisory post-commit hook) and swept inbox items into `todo.md`. Push hash: bccaacaa41a803e672e8f48c0c21c85226abf3c8. Logging commit: 52a104902f4e297fd3580fa1f407ef34061e1606. Snapshot: rev_010_current. Skill: none. (ledger: 2025-12-27T23:51:38-08:00 — Push enforcement hardening).
- Added Design Intent Schema concept (spec, schema, validator, tests, lifecycle docs). Spec: 193e018f-6875-4276-b503-2af48f6ec37b. Skill: none. Stack: Python. (ledger: 2025-12-26T00:23:48-08:00 — Design Intent Schema concept).
- Added human-friendly glossary and concepts map, linking them from README, HUMAN_START_HERE, and the wiki index. Skill: none. (ledger: 2025-12-24T13:58:44-08:00 — Human-friendly glossary and wiki clarifications).
- Added context management deep dive doc and linked it from README and the wiki index. Skill: none. (ledger: 2025-12-24T13:58:44-08:00 — Human-friendly glossary and wiki clarifications).
- Emphasized the `HUMAN_START_HERE.md` entrypoint in README quick start and cleared the inbox request. Skill: none. (ledger: 2025-12-24T13:58:44-08:00 — Human-friendly glossary and wiki clarifications).
- Added spec-compiler-enforcement CI workflow requiring spec-generation-framework provenance, validation, Codex prompt consumption checks, and compiler drift detection. Skill: none. (ledger: 2025-12-24T18:15:02-08:00 — Spec compiler CI enforcement).
- Rewrote the context management rationale with a structured, falsifiable section for reducing context pressure and enabling resumable workflows. Skill: none. (ledger: 2025-12-24T23:46:09-08:00 — Context window benefits documentation).
- Added a plain-English note in README that the chat window stays lean because state is externalized (limits still apply). Skill: none. (ledger: 2025-12-24T23:53:34-08:00 — README plain-English context window note).
- Added beginner-friendly entry points to README and HUMAN_START_HERE and simplified human guides/cheat sheet for quick onboarding. Skill: none. (ledger: 2025-12-24T23:57:00-08:00 — Human docs clarity pass).
- Executed prompt followups 8-9 (README spec-driven governance docs, HUMAN_START_HERE update, README governance CI bridge, new-repo bootstrap Skill) and removed the prompt files. Skill: none. (ledger: 2025-12-24T13:36:38-08:00 — Prompt followup execution (README governance)).
- Executed prompt followups 5-7 (README rewrite, README lint autofix + quality CI, README rubric + lint guide) and removed the prompt files. Skill: none. (ledger: 2025-12-24T13:23:53-08:00 — README governance followups).
- Processed `todo-inbox.md` update (queued `prompt_followup9.md`) and confirmed readme-spec-engine repo is unavailable; prompt followups 8-9 are blocked. Skill: none. (ledger: 2025-12-24T13:36:38-08:00 — Prompt followup execution (README governance)).
- Executed prompt followups 1-4 (doc profiles + pre-commit hook, codex doc rewrite prompt, internal-notes profile, profile summary table, ui_governance skill package + tests, and UI governance validators) and removed the prompt files. Skill: ui_governance. (ledger: 2025-12-24T12:54:26-08:00 — Prompt followup execution).
- Implemented the Structured Richness documentation system (spec, markdownlint + Vale configs, templates) and moved follow-up prompts into `todo.md`. Skill: none. (ledger: 2025-12-24T12:43:00-08:00 — Structured Richness documentation system).
- Pushed commit `6be59ff` to `origin/master` per request. Skill: none. (ledger: 2025-12-24T12:30:34-08:00 — Git push (housekeeping)).
- Confirmed the UI intent Skill manifest and PDCA loop locations for the UI intent system. Skill: none. (ledger: 2025-12-24T12:27:50-08:00 — UI intent protocol confirmation (Skill + PDCA)).
- Explained what `scripts/check-invariants.sh` and `scripts/check-uip-compliance.sh` do for local enforcement validation. Skill: none. (ledger: 2025-12-24T12:21:58-08:00 — Script explanation (UIP enforcement checks)).
- Executed `prompt_ci_retests.md` (enforcement audit runner, quarterly CI workflow, audit artifacts, gitignore update, workflow audit entries) and captured snapshot `rev_008_current`; removed the prompt. Skill: none. (ledger: 2025-12-24T10:28:20-08:00 — Prompt Task Execution Queue).
- Executed `prompt_flywheel_phase3.md` (Fast/Safe scope enforcement, run metadata fields, execution profile doc + invariants update, workflow audit entries) and captured snapshot `rev_007_current`; removed the prompt. Skill: none. (ledger: 2025-12-24T10:28:20-08:00 — Prompt Task Execution Queue).
- Executed `prompt_flywheel_phase2.md` (run receipt schema/field alignment, append-outcome helper, CI diff enforcement tweak, AGENTS note update, workflow audit entry) and captured snapshot `rev_006_current`; removed the prompt. Skill: none. (ledger: 2025-12-24T10:28:20-08:00 — Prompt Task Execution Queue).
- Updated UIP documentation/navigation (enforcement notes, renderer compliance link, wiki index) and captured workflow snapshot `rev_005_current`. Skill: none. (ledger: 2025-12-24T11:37:16-08:00 — Documentation update (UIP additions)).
- Executed `prompt_additional_items5.md` (event→sync validation, renderer certification harness + docs, UIP-0.2 shadow schemas + reporting, CI ordering updates, README update, sync examples) and removed it. Skill: none. (ledger: 2025-12-24T10:28:20-08:00 — Prompt Task Execution Queue).
- Executed `prompt_additional_items4.md` (schema-aware UIP discovery + validation, boundary checks, enforcement/README updates, CI label tweak, payload updates) and removed it. Skill: none. (ledger: 2025-12-24T10:28:20-08:00 — Prompt Task Execution Queue).
- Added workflow reminders for GitHub pushes + documentation updates, updated the workflow audit log, and captured snapshot `rev_004_current`. Skill: none. (ledger: 2025-12-24T11:03:58-08:00 — Workflow reminders (push + documentation)).
- Executed `prompt_additional_items3.md` (added `docs/ui-protocol/migrations/UIP-0.2-strawman.md`) and removed it. Skill: none. (ledger: 2025-12-24T10:28:20-08:00 — Prompt Task Execution Queue).
- Executed `prompt_additional_items2.md` (expanded UIP forbidden-output scan tokens + enforcement README update) and removed it. Skill: none. (ledger: 2025-12-24T10:28:20-08:00 — Prompt Task Execution Queue).
- Executed `prompt_additional_items1.md` (UIP enforcement scripts + CI hook, migration guide template, renderer compliance checklist, UIEvent schema updates) and removed it. Skill: none. (ledger: 2025-12-24T10:28:20-08:00 — Prompt Task Execution Queue).
- Executed `prompt_enforcement_slowdown_optimization.md` (no changes; conflicts with existing enforcement hardening) and removed it. Skill: none. (ledger: 2025-12-24T10:28:20-08:00 — Prompt Task Execution Queue).
- Executed `prompt_flywheel2_enforcement_layer_audit.md` (file was empty) and removed it. Skill: none. (ledger: 2025-12-24T10:28:20-08:00 — Prompt Task Execution Queue).
- Executed `prompt_flywheel1.md` (invariant enforcement scripts, run record schema + helper, execution profiles doc, AGENTS update, CI workflow, preflight checks), removed `prompt_flywheel1.md`, and captured workflow snapshot `rev_003_current`. Skill: none. (ledger: 2025-12-24T10:28:20-08:00 — Prompt Task Execution Queue).
- Executed `prompt2.md` (added `docs/ui-protocol/UIP-0.1.md`) and removed `prompt2.md`. Skill: none. (ledger: 2025-12-24T10:28:20-08:00 — Prompt Task Execution Queue).
- Executed `prompt1.md` (UI skill entry add-ons, UI event sync template, Tailwind pattern library plugin) and removed `prompt1.md`. Skill: none. (ledger: 2025-12-24T10:28:20-08:00 — Prompt Task Execution Queue).
- Processed `todo-inbox.md` follow-up and moved the new documentation update item into `todo.md`. Skill: none. (ledger: 2025-12-24T10:23:16-08:00 — Todo Inbox Processing (Follow-up)).
- Processed `todo-inbox.md` and moved prompt execution items into `todo.md`. Skill: none. (ledger: 2025-12-24T10:21:35-08:00 — Todo Inbox Processing).
- Implemented UI intent protocol infrastructure (schema/types + JSON Schema, Tailwind adapter contract + reference renderer, UI intent Skill package, PDCA loop, wiki summaries). Skill: none (new Skill ui_intent.emit added). (ledger: 2025-12-24T09:35:09-08:00 — UI Intent Protocol Infrastructure).
- Documented the handover purpose (context reset for small LLM windows) in README and the workflow guide; captured local snapshot `rev_002_current`. Skill: none. (ledger: 2025-12-22T15:57:05-08:00 — Handover purpose docs + README prominence).
- Added README snapshot section note that users can ask the agent to update the framework to fit the project; captured local snapshot `rev_001_current`. Skill: none. (ledger: 2025-12-22T15:19:54-08:00 — README change request confirmation).
- Simplified quick-start header to “any agentic frontend (Codex, Gemini, Claude/Anthropic, Grok, etc.)” and captured local snapshot `rev_043_current`. Skill: none. (ledger: 2025-12-22T14:57:37-08:00 — Quick-start header phrasing).
- Clarified quick-start usage across Codex and other agentic frontends, kept the framework as the source of truth, and captured local snapshot `rev_042_current`. Skill: none. (ledger: 2025-12-22T14:44:26-08:00 — Quick-start provider guidance).
- Reworded quick-start prompt to instruct applying the public framework for new and existing projects; captured local snapshot `rev_041_current`. Skill: none. (ledger: 2025-12-22T14:38:20-08:00 — Quick-start prompt rewording).
- Updated quick-start prompts to instruct cloning `holaymolay/governance-orchestrator` if missing and to use the repo root; captured local snapshot `rev_040_current`. Skill: none. (ledger: 2025-12-22T14:28:02-08:00 — Quick-start clone instructions).
- Added repo link and clone snippet to quick-start prompts and captured local snapshot `rev_039_current`. Skill: none. (ledger: 2025-12-22T14:25:44-08:00 — Add repo link for LLM quick-start).
- Updated quick-start prompts to reference `holaymolay/governance-orchestrator` and captured local snapshot `rev_038_current`. Skill: none. (ledger: 2025-12-22T14:23:09-08:00 — Update quick-start repo reference).
- Propagated the official title "Context-Engineering Framework for Coding Agents" across human entrypoints and guides, and captured local snapshot `rev_037_current`. Skill: none. (ledger: 2025-12-22T13:36:34-08:00 — Propagate official framework title).
- Provided dictionary-word acronym options using the provided letter set with `CE` kept together. Skill: none. (ledger: 2025-12-22T11:26:38-08:00 — Acronym options from letter set).
- Added `HUMAN_START_HERE.md`, linked it in README/wiki/human docs, updated snapshot guidance/tooling, and captured local snapshot `rev_035_current`. Skill: none. (ledger: 2025-12-22T10:52:19-08:00 — Human entrypoint + snapshot inclusion).
- Added AI-managed headers to agent-owned files, expanded README with AI-operated guidance + quick-start prompt + model requirements, published `docs/humans/about.md`, and captured local snapshot `rev_034_current`. Skill: none. (ledger: 2025-12-22T10:47:21-08:00 — AI-managed banners + README clarity + About doc).
- Added AI-operated guidance and AI-managed guardrails, aligned framework vs workflow terminology across governance docs, and captured local snapshot `rev_033_current`. Skill: none. (ledger: 2025-12-22T10:16:10-08:00 — AI-only operation clarifications + terminology pass).
- Clarified who runs workflow snapshot scripts and confirmed framework vs workflow terminology guidance. Skill: none. (ledger: 2025-12-22T10:08:54-08:00 — Clarify script ownership + terminology guidance).
- Rewrote README for a human audience, clarified framework vs workflow terminology, updated `.gitignore` to keep workspace files ignored, and captured local snapshot `rev_031_current`. Skill: none. (ledger: 2025-12-22T10:02:46-08:00 — README public introduction + terminology pass).
- Stopped tracking `ai_workflow_revisions/` in git, added `docs/workflow-revisions.md`, updated snapshot guidance/tooling, and captured local snapshot `rev_030_current`. Skill: none. (ledger: 2025-12-22T10:12:18-08:00 — Untrack workflow revision snapshots).
- Added a one-sentence project description to README, updated governance logs, and captured workflow snapshot `rev_029_current`. Skill: none. (ledger: 2025-12-22T09:30:34-08:00 — Add public repo description).
- Moved human instruction docs into `docs/humans/`, updated references/tooling, and captured workflow snapshot `rev_028_current`. Skill: none. (ledger: 2025-12-22T02:04:15-08:00 — Move human docs into docs/humans).
- Added quick-apply adoption phrase + checklist, updated bootstrap tooling and audit log, and captured workflow snapshot `rev_027_current`. Skill: none. (ledger: 2025-12-22T01:13:11-08:00 — Quick apply adoption request).
- Added user guide cheat sheet `docs/humans/user-guide-cheat-sheet.md`, linked it in governance docs/wiki, updated audit log, and captured workflow snapshot `rev_026_current`. Skill: none. (ledger: 2025-12-22T01:04:41-08:00 — User guide cheat sheet).
- Added human user guide `docs/humans/user-guide.md`, linked it in governance docs/wiki, updated audit log, and captured workflow snapshot `rev_025_current`. Skill: none. (ledger: 2025-12-22T01:01:18-08:00 — Human user guide for AI workflow).
- Added baseline speed/accuracy metrics to `docs/workflow-audit.md`, recorded the baseline audit entry, and captured workflow snapshot `rev_024_current`. Skill: none. (ledger: 2025-12-22T00:55:37-08:00 — Workflow audit baseline metrics).
- Added workflow audit log with Improvement Gate and speed/accuracy templates, updated governance/docs/wiki, and captured workflow snapshot `rev_022_current`. Skill: none. (ledger: 2025-12-22T00:36:18-08:00 — Workflow audit loop (speed + accuracy)).

- Added a housekeeping fast-path rule for routine requests like `git push` and captured workflow snapshot `rev_021_current`. Skill: none. (ledger: 2025-12-22T00:30:51-08:00 — Housekeeping fast-path rule).
- Added Reasoning Skills validator script, documented the log checklist, updated guidance, and captured workflow snapshot `rev_020_current`. Skill: none. (ledger: 2025-12-22T00:24:02-08:00 — Reasoning Skills validator + log checklist).
- Added Reasoning Skills layer (spec `specs/reasoning-skills-layer-v1.md`), created reasoning schema/manifests/pipeline, updated governance docs/wiki, and captured workflow snapshot `rev_019_current`. Skill: none. (ledger: 2025-12-22T00:13:30-08:00 — Reasoning Skills layer implementation).
- Added Clarification Gate governance (spec `specs/clarification-gate-v1.md`), updated workflow docs/wiki, and captured workflow snapshot `rev_018_current`. Skill: none. (ledger: 2025-12-22T00:05:31-08:00 — Clarification Gate integration).
- Recommended when to adopt the Reasoning Skills layer and outlined contraindications. Skill: none. (ledger: 2025-12-21T22:11:25-08:00 — Reasoning Skills recommendation).
- Outlined mitigations for a Reasoning Skills layer to preserve guarantees while reducing friction. Skill: none. (ledger: 2025-12-21T22:08:03-08:00 — Reasoning Skills mitigations).
- Pushed recent workflow documentation updates (Decision Queue example + neutral wording) to `origin/master`. Skill: none. (ledger: 2025-12-21T17:24:13-08:00 — Commit and push workflow updates).
- Added a Decision Queue example, clarified Decision Queue placement, removed organization-specific references, and captured workflow snapshot `rev_017_current`. Skill: none. (ledger: 2025-12-21T17:20:32-08:00 — Decision queue example + neutral wording).
- Added Decision Queue sections to `todo.md`/`todo-inbox.md`, updated bootstrap templates, documented the queue in playbooks, and captured workflow snapshot `rev_016_current`. Skill: none. (ledger: 2025-12-21T17:12:24-08:00 — Decision queue templates + playbook).
- Clarified Decision Queue behavior, made Continuous Mode the default, updated governance docs, and captured workflow snapshot `rev_015_current`. Skill: none. (ledger: 2025-12-21T17:08:01-08:00 — Decision queue + default mode).
- Defined Continuous Mode and Iterative Mode in governance docs, clarified Continuous Execution Mode, and captured workflow snapshot `rev_014_current`. Skill: none. (ledger: 2025-12-21T17:00:38-08:00 — Workflow operating modes).
- Added a workflow adoption copy-list appendix, created `scripts/bootstrap-workflow.sh`, and captured workflow snapshot `rev_013_current`. Skill: none. (ledger: 2025-12-21T16:54:07-08:00 — Workflow adoption enhancements).
- Added workflow adoption guide (`docs/humans/workflow-adoption.md`), updated navigation/snapshot tooling, and captured workflow snapshot `rev_012_current`. Skill: none. (ledger: 2025-12-21T16:24:44-08:00 — Workflow adoption documentation).
- Explained how to select and apply stack profiles when starting a new project. Skill: none. (ledger: 2025-12-21T16:21:47-08:00 — Stack invocation guidance).
- Clarified which parts of the AI workflow are stack-specific versus project-specific. Skill: none. (ledger: 2025-12-21T16:17:15-08:00 — Workflow specificity clarification).
- Established stack-agnostic governance with todo/backlog/completed/handover/CHANGELOG scaffolding.
- Added comprehensive stack profile set and navigation across AGENTS/wiki plus stack quickstart playbook updates.
- Added a frontend UI/UX-specific Skill idea list (`docs/skills/skill-ideas-ui-ux.md`).
- Added a brainstorming list of candidate reusable Skills to guide building a comprehensive library (`docs/skills/skill-ideas.md`).
- Added `skillctl scaffold` helper and generated an initial upstream Skill Card catalog for Anthropic source skills.
- Added Skill `skillcard.index` to deterministically discover and summarize `SKILL.md` Skill Cards.
- Added Skill `skillcard.parse` to parse/validate upstream `SKILL.md` Skill Cards (Anthropic/Claude + OpenAI Codex formats) for ingestion workflows.
- Updated stored Codex Skill Library master prompt (added Success Criteria), captured snapshot `rev_011_current`, and updated baseline pointers.
- Added `skillctl` runner v1 + setup/test scripts, added foundational Skill `fs.hash_tree`, and captured snapshot `rev_010_current`.
- Added AgentFS enforcement layer spec and artifacts (layout, access matrix, invariants, reference implementation, migration plan) under `specs/` and `docs/agentfs/` (ledger: 2025-12-20 — AgentFS Enforcement Layer Integration).
- Completed a repository review focused on governance and Skill compliance gaps (ledger: 2025-12-21 — Repository review (governance + Skills)).
- Synced curated OpenAI skills via skill-installer and added spec `specs/openai-skills-sync-v1.md` (ledger: 2025-12-21 — OpenAI skills sync).

## Next Steps
- Maintain pre/post-task sweeps of `todo-inbox.md`; keep todos/backlog/completed/handover agent-managed.
- When modifying workflow/governance docs, create the next local `ai_workflow_revisions/rev_00X_current` snapshot (per `docs/workflow-revisions.md`) and log the revision in `completed.md`, `CHANGELOG.md`, and `handover.md`.
- Record new work in the planner ledger (`docs/context/planner-task-manager.md`) before coding and close entries with outcomes.
- If needed, run the UI intent Skill smoke test (`skills/ui-intent-emit/tests/test_smoke.sh`) or `scripts/skillctl validate --all`.
- Implement AgentFS runtime enforcement per `specs/agentfs-enforcement-layer-v1.md`, starting with Phase 1 PDCA gating.

## Pending Items
- None.
