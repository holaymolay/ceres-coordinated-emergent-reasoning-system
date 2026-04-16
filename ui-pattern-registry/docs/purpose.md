# Purpose

The UI Pattern Registry is a machine-readable catalog of allowable UI structures for LLM-driven front-end systems. It defines what structural patterns exist, when they can be used, and how they compose—so agents select from a finite vocabulary instead of inventing layouts.

## Goals
- Reduce layout variance by constraining generation to explicit, named patterns.
- Prevent structural hallucination by declaring required parts, usage contexts, and nesting limits.
- Keep definitions renderer-agnostic so multiple adapters can enforce the same structures.
- Make validation deterministic via schemas, scripts, and CI gates.

## Non-goals
- Style tokens (spacing, color, typography) or component implementations.
- Framework-specific markup (React/Vue/HTML) or renderer glue code.
- Prompt libraries, agent workflows, or design intent definitions.
- Workflow automation beyond schema + pattern declarations.

## Working principles
- Patterns are structural contracts: required parts, optional variants, composability rules, and usage constraints.
- Everything is machine-readable and validated against `schemas/pattern.schema.json`.
- Allow/forbid rules travel with the pattern definition; enforcement lives in consuming systems and CI.
- Explicit beats implicit: if a structure is not in this registry, it should not appear in generated output.
