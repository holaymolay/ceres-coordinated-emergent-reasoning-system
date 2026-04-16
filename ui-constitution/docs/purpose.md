# Purpose

This repository defines a Visual Constitution: a machine-readable body of law that constrains visual design outputs.
It exists to provide deterministic, enforceable limits so LLM-generated UIs remain consistent, auditable, and safe to iterate.

Scope:
- Visual constraints only (typography, spacing, color roles, elevation, radius, motion, assets).
- No UI components, layouts, renderers, or framework-specific tokens.
- No agent logic, prompts, or workflow definitions beyond governance files.

The constitution is expressed as JSON Schema documents under `constitution/` and is designed to be consumed by compilers, CI checks, and renderers.
