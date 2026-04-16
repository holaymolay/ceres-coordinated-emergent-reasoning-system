# Human Start Here

**Hub entry:** Load CERES via the umbrella `PROMPTLOADER.md` + `CONSTITUTION.md` (hub repo) and use hub todo templates/init script when bootstrapping; this component stays independent and is pulled via hub clone/run scripts.


This repository is the CERES UI Constitution subcomponent.
It is AI-operated: humans provide goals and decisions; the agent runs scripts and updates AI-managed files.

## Quick Start (Copy/Paste Prompt)
Paste this into any agentic frontend (Codex, Gemini, Claude/Anthropic, Grok, etc.) and add your task:

```text
You are to incorporate this CERES for Coding Agents, located at https://github.com/holaymolay/governance-orchestrator, as the governance framework for this project.

For new projects, implement this framework from the start. Once the framework is in place I will describe the project and its requirements.
For existing projects, implement this framework and bring the existing codebase into compliance with the framework.

Read `AGENTS.md` and treat it as the authoritative contract.
Operate in AI-only mode: run scripts yourself and update AI-managed files; humans only add tasks via chat or `todo-inbox.md`.

If your provider has built-in governance features, use this framework as the source of truth and integrate with those features as needed.

## If you are new (3 steps)
- Read `docs/humans/user-guide-cheat-sheet.md` (one page).
- Paste the quick-start prompt above into your agent and add your goal.
- Keep tasks and decisions in chat or `todo-inbox.md`; let the agent handle the rest.
```

## Where Humans Should Act
- Use chat or `todo-inbox.md` to submit tasks and decisions.
- Do not edit AI-managed files: `todo.md`, `backlog.md`, `completed.md`, `handover.md`, `CHANGELOG.md`.
- Use `docs/humans/glossary.md` when a term is unfamiliar; use `docs/humans/concepts-map.md` to jump to authoritative docs.

## README governance
Humans author `README_SPEC.yaml` when defining new projects; agents may draft it only when directed and must keep humans in the loop.
Agents must never free-write `README.md`; they invoke `readme-spec-engine` to generate from the spec and then run enforcement checks.
When the spec changes, regenerate the README externally and rerun the enforcement scripts.

## Model Requirements (Short)
- Works from a local clone with no web access unless the task needs it.
- Must be able to read/write files and run shell commands via a CLI or IDE agent.
- Built and tested with OpenAI Codex; intended to work with any frontier-quality LLM, but broader validation is still needed.

## Learn More
- `README.md` (overview + decision tree)
- `docs/humans/user-guide.md` (how to structure requests)
- `docs/humans/workflow-guide.md` (framework overview)
- `docs/humans/workflow-adoption.md` (apply to a new project)
- `docs/humans/about.md` (background and evolution)
- `docs/humans/glossary.md` (definitions and clickable links)
- `docs/humans/concepts-map.md` (navigation map)