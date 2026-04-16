Spec Title: Visual Constitution v0.1.0 (governance + schema set)
Spec ID: 85a44460-bd37-40d4-89e2-7f2d750ab755
User Story: As a compiler/CI/rendering integrator, I need a machine-readable visual constitution so that UI outputs can be validated deterministically against enforceable aesthetic constraints.

Functional Requirements:
- Provide JSON Schema documents for typography, spacing, color, elevation, radius, motion, and assets constraints under /constitution.
- Include a top-level constitution schema that references the domain schemas and requires a semver version field.
- Define explicit, machine-enforceable limits (enumerations, bounds, maxima) with no subjective wording.
- Provide documentation for purpose, enforcement model, versioning, and example valid/invalid snippets.
- Integrate the Context-Engineering Framework governance artifacts and workflow logs.

Non-functional Requirements:
- No framework coupling; schemas must be renderer-agnostic.
- No defaults that imply taste; avoid subjective language.
- ASCII-only edits unless existing files require Unicode.

Architecture Overview:
- The repository is a spec-only artifact: JSON Schema files under /constitution and docs under /docs.
- Governance framework artifacts live at repo root and /docs per AGENTS.md.
- A semver version string in the constitution object anchors compatibility for downstream tools.

Language & Framework Requirements:
- JSON Schema draft 2020-12.
- No application runtime.

Testing Plan:
- Validate schema documents compile with a standard JSON Schema validator (manual verification).
- Validate example snippets against the schemas using any compliant validator (manual check).

Dependencies:
- None in-repo; downstream users provide JSON Schema validators.

Input/Output Schemas:
- Input: constitution documents validated against constitution/constitution.schema.json.
- Domain schema references: constitution/typography.schema.json, constitution/spacing.schema.json, constitution/color.schema.json, constitution/elevation.schema.json, constitution/radius.schema.json, constitution/motion.schema.json, constitution/assets.schema.json.

Clarifications (optional):
- Q: Which repo name should be used? A: ui-constitution (per workspace path).
- Q: Which schema format? A: JSON Schema draft 2020-12.

Validation Criteria:
- All schema files are present and referenceable from the top-level constitution schema.
- Documentation exists at docs/purpose.md, docs/enforcement-model.md, docs/versioning.md.
- Example snippets include clear valid vs invalid JSON.
- Governance artifacts (todo, completed, handover, changelog, run records) are updated.

Security Constraints:
- No external calls without approved connectors.
- Validate all schema inputs before use in downstream automation.
