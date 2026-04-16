# UI Intent Protocol (Concept)

## Purpose
Provide a minimal, extensible protocol for agents to emit UI intent objects that are rendered exclusively by the adapter layer.

## Boundaries
- Intent schema and examples are framework-agnostic.
- Adapter layer owns rendering and tokenized Tailwind usage.
- Reference renderer consumes validated intent output only.

## Folder structure
- handlers/intent: TypeScript intent types, validation helpers, JSON Schema, and examples.
- handlers/adapter: Adapter contract, token map, layout patterns, and React renderer (JSX confined here).
- handlers/reference: Example intent JSON and the reference render flow.

## Example rendered output
- The reference form intent renders a titled form with two fields (first name, role) and two actions (submit and cancel).
