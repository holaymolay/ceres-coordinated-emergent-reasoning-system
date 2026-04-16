# UI Intent Protocol

This playbook summarizes how to use the UI intent protocol and its governing Skill. It is navigation-only; authoritative sources are referenced below.

## Quick Path
1. Author intents using the schema in `concepts/ui-intent-protocol/handlers/intent/intent-schema.ts` (JSON Schema: `concepts/ui-intent-protocol/handlers/intent/intent.schema.json`).
2. Apply UI governance via Skill `ui_governance` (`skills/ui-governance/`).
3. Validate intent emission via Skill `ui_intent.emit` (`skills/ui-intent-emit/`).
4. Render via the adapter in `concepts/ui-intent-protocol/handlers/adapter/tailwind-adapter.tsx`.
5. Apply PDCA changes through schema/pattern/token updates (`concepts/ui-intent-protocol/pdca.md`).

## Authoritative References
- Concept: `concepts/ui-intent-protocol/manifest.yaml`
- Schema & examples: `concepts/ui-intent-protocol/handlers/intent/`
- Adapter contract: `concepts/ui-intent-protocol/handlers/adapter/`
- Skills: `skills/ui-governance/skill.yaml`, `skills/ui-intent-emit/skill.yaml`
- PDCA loop: `concepts/ui-intent-protocol/pdca.md`
