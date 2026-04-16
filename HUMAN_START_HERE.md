# Human Start Here

**Hub entry:** Load CERES via the umbrella `PROMPTLOADER.md` + `CONSTITUTION.md` (hub repo) and use hub todo templates/init script when bootstrapping; this component stays independent and is pulled via hub clone/run scripts.


This repository is the CERES README Spec Engine subcomponent.
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
```

## Where Humans Should Act
- Use chat or `todo-inbox.md` to submit tasks and decisions.
- Do not edit AI-managed files: `todo.md`, `backlog.md`, `completed.md`, `handover.md`, `CHANGELOG.md`.

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