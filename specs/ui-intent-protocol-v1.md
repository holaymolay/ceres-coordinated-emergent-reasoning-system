Spec Title: UI Intent Protocol v1 (Agent-to-UI Infrastructure)
Spec ID: d520edbb-18e7-4b29-834c-6756329b2c81
Skill: none (new Skill ui_intent.emit to be added)
User Story: As a delivery team, I need a governed UI intent protocol that agents can emit as structured data so UI rendering remains adapter-controlled, auditable, and refinable via PDCA.

Functional Requirements:
- Define a minimal, extensible UI intent schema supporting page.create, form.create, table.create, modal.open, alert.show, and cta.request.
- Provide TypeScript types plus a JSON Schema for validation; include example intent objects.
- Define a Tailwind adapter contract that resolves intent -> layout pattern -> component mapping using semantic tokens only.
- Provide a reference implementation that renders a form intent through the adapter with React; JSX is restricted to the adapter layer.
- Define a deterministic Skill manifest that validates and emits UI intent artifacts only (no JSX/HTML/Tailwind output).
- Define a PDCA loop for UI refinement that only adjusts intent schema, token maps, and layout patterns.

Non-functional Requirements:
- Intent payloads must be JSON-serializable and versioned.
- Agents must not output JSX/HTML/CSS/Tailwind classes; rendering authority lives in the adapter.
- Tailwind usage is centralized in adapter token maps (no raw classes outside adapter).
- Keep the system minimal and extensible; avoid over-engineering or design-system scope creep.

Architecture Overview:
- Concept: `concepts/ui-intent-protocol/` holds schema, adapter contract, and reference renderer.
- Skill: `skills/ui-intent-emit/` validates incoming intent objects against the JSON Schema and outputs validated artifacts.
- PDCA artifacts: `concepts/ui-intent-protocol/pdca.md` defines Plan/Do/Check/Act for controlled UI refinement.

Language & Framework Requirements:
- TypeScript for schema/types and adapter contract.
- React used only within the adapter implementation (reference renderer consumes adapter output).
- Tailwind classes must be resolved via token maps inside the adapter.

Testing Plan:
- Validate `skills/ui-intent-emit/skill.yaml` with `scripts/skillctl validate --all` when available.
- Use schema validation on the example intent objects (manual or via skill run).
- Spot-check the reference renderer flow (intent -> validate -> adapter render).

Dependencies:
- None required beyond the existing repository runtime assumptions.

Input/Output Schemas:
- UI intent JSON Schema: `concepts/ui-intent-protocol/handlers/intent/intent.schema.json`.
- Skill input/output schemas: `skills/ui-intent-emit/schemas/input.schema.json` and `skills/ui-intent-emit/schemas/output.schema.json`.

Clarifications (optional):
- None.

Validation Criteria:
- TypeScript intent interfaces and JSON Schema exist and align on required fields.
- Tailwind adapter contract defines tokens, layout patterns, and component mappings with centralized token usage.
- Reference implementation shows a validated form intent flowing through the adapter without JSX outside the adapter layer.
- Skill manifest declares deterministic, stateless validation and forbids JSX/HTML/Tailwind output.
- PDCA definition enumerates Plan/Do/Check/Act artifacts and observability hooks.

Security Constraints:
- No network access or secret handling.
- Skills must declare minimal access (stdout-only) and remain deterministic.
