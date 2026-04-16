# README governance

The README is a governed artifact generated from a spec, not free prose.
This document defines the boundaries between spec, generator, and enforcement.
It keeps README changes deterministic while preserving human review.
Follow these rules before any README change lands.

## Governed artifacts
- `README_SPEC.yaml` is the single source of truth for README content.
- `README.md` is generated from the spec by `readme-spec-engine`.
- This repository enforces structure and narrative quality; it does not generate content.

> NOTE: Never edit `README.md` directly. Update `README_SPEC.yaml`, regenerate externally, then enforce.

## Lifecycle
1. Draft or update `README_SPEC.yaml` with the desired narrative.
2. Run `readme-spec-engine` outside this repo to generate `README.md`.
3. Commit both files together.
4. Run README enforcement checks (lint + governance CI) to validate structure and compliance.

## Roles and boundaries
- Generation: `readme-spec-engine` (external project) turns specs into README content.
- Enforcement: this framework validates presence, structure, and governance of the generated README.
- Agents: must not free-write the README and must keep spec and README in sync.
- Humans: may author specs and review generated output before enforcement.
