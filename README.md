# Context Engineering Framework (Umbrella)

This repository is the coordination entrypoint for the Context Engineering Framework ecosystem. It is **not** a monorepo and does **not** execute tools or enforce rules; all enforcement and runtime behavior live inside the individual component repositories.

## Component Repositories
- `cef-governance-orchestrator`: Governance and context-engineering framework for operating coding agents.
- `cef-readme-spec-engine`: Spec-driven README generator and validator for deterministic documentation.
- `cef-spec-compiler`: Compiler-style CLI that turns clarified intent into governed specification artifacts.
- `cef-ui-constitution`: Machine-readable visual constitution defining enforceable UI constraints.
- `cef-ui-pattern-registry`: Registry of approved UI patterns for renderer-agnostic, LLM-driven front ends.

## Workspace Model
- Parent (this repo): coordination map, docs, and lightweight scripts only.
- Children (`cef-*`): independent tools with their own governance, tests, and release cycles.
- Git ignores children by design; no child content is tracked here, and removal of this repo must not affect runtime behavior of any component.
