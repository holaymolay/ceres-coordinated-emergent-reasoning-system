# CERES UI Constitution
Part of the CERES (Coordinated Emergent Reasoning System). Umbrella repo: [CERES](https://github.com/holaymolay/ceres-coordinated-emergent-reasoning-system).
**Hub entry:** Load CERES via the umbrella `PROMPTLOADER.md` + `CONSTITUTION.md` (hub repo) and use hub todo templates/init script when bootstrapping; this component stays independent and is pulled via hub clone/run scripts.




## Why This Exists

Machine-readable Visual Constitution that defines enforceable constraints for LLM-generated UI systems.

## Audience

**Include**
- Compiler and CI pipeline integrators who need deterministic visual rules.
- Frontend renderers that validate visual constraints before output.

**Exclude**
- Teams looking for UI components or framework-specific tokens.
- Projects seeking prompts or agent workflows.

## Problem

Without enforceable constraints, LLM-generated UIs drift in style, violate accessibility floors, and become inconsistent across iterations.

## Solution

Publish a schema-governed constitution that encodes hard visual limits (typography, spacing, color, motion, assets) for deterministic validation.

## Outcomes

Expected outcomes:

- Provide JSON Schema documents for each visual domain with explicit bounds.
- Enable automated validation in CI and rendering pipelines.
- Define versioned, machine-enforceable rules with clear violation semantics.

## Quick Start

Run these steps:

1. Read docs/purpose.md to understand scope and intent.
2. Validate a constitution document against constitution/constitution.schema.json.
3. Consult docs/enforcement-model.md for violation handling semantics.

## Repository Map

| Path | Description | Exists |
| --- | --- | --- |
| constitution/ | JSON Schema documents that define the Visual Constitution. | yes |
| docs/ | Purpose, enforcement, versioning, and governance documentation. | yes |
| specs/ | Task specs and governance artifacts for changes. | yes |
| skills/reasoning/ | Reasoning manifests required by the governance framework. | yes |
| scripts/ | Workflow and run-record helper scripts. | yes |

## Non-Goals

This tool explicitly avoids:

- Not a UI component library.
- Not a renderer or design system implementation.
- Not a prompt collection or agent framework.

## Constraints

Hard constraints:

- Max length: 5200 chars
- Banned terms: None
- Tone profile: neutral
## Observability (local)
- Use  to emit stage events via hub .
