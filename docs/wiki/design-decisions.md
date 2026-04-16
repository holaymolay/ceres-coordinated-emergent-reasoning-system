# Design Decisions

This page logs notable architectural decisions. It is a wiki summary and does not override authoritative specs/manifests.

## 2025-12-24 — UI Intent Protocol Infrastructure
- Decision: Introduce a concept-bound UI intent protocol (schema + adapter + reference renderer) governed by a deterministic Skill for intent emission.
- Rationale: Keeps agents emitting structured intent only, while rendering stays adapter-controlled and refinable through PDCA.
- Authoritative references: `specs/ui-intent-protocol-v1.md` (Spec ID: `d520edbb-18e7-4b29-834c-6756329b2c81`), `concepts/ui-intent-protocol/manifest.yaml`, `skills/ui-governance/skill.yaml`, `skills/ui-intent-emit/skill.yaml`.

## 2025-12-15 — Deterministic Skill System (Skill Library v1)
- Decision: Treat Skills as deterministic, stateless tool packages with schema-defined JSON stdin/stdout, executable without any LLM.
- Rationale: Makes Skills testable and portable across Codex/GPT/Claude/MCP/CLI; keeps reasoning/orchestration in agents, not in Skills.
- Authoritative references: `specs/skill-library-v1.md` (Spec ID: `6f34688b-a76e-46b8-8d2d-8ffe5c88f9c6`), `docs/skills/skill-library-v1.md`.
