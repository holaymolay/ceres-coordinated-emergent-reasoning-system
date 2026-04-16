# Patterns

This page summarizes reusable patterns discovered during delivery. It is a navigation layer and does not override authoritative specs/manifests/Skills.

## Skill Packages
- Use `skills/<skill-slug>/` with `skill.yaml`, `schemas/`, `impl/`, `tests/`, and `fixtures/`.
- Keep Skill implementations deterministic and stateless; declare access in `skill.yaml` and follow `docs/access-manifest.md`.
- Prefer stdout-only Skills; avoid filesystem writes unless explicitly required and reviewed.

Authoritative reference: `docs/skills/skill-library-v1.md` (spec: `specs/skill-library-v1.md`).

## UI Intent Protocol
- Intent schema, adapter contract, and reference renderer live under `concepts/ui-intent-protocol/`.
- Skill `ui_intent.emit` validates intent emission (`skills/ui-intent-emit/`).
- Skill `ui_governance` governs UI intent constraints and capability usage (`skills/ui-governance/`).
- PDCA loop for UI refinement is defined in `concepts/ui-intent-protocol/pdca.md`.
