# New repo bootstrap (spec-first README)

Use this Skill contract when creating a new repository so README content stays spec-driven and enforced. It is deterministic and bans free-written README prose.

## Invariant workflow
1. Spec first: create `README_SPEC.yaml` describing the narrative and structure.
2. Deterministic generation: run `readme-spec-engine generate` to produce `README.md` from the spec only.
3. Governance wiring: add README governance CI and align with the context-engineering enforcement layer.
4. Stop: do not hand-edit `README.md`; future changes require spec updates and regeneration.

## Fail conditions
- `README_SPEC.yaml` is missing or not committed.
- `README.md` was authored or edited manually.
- Generator was invoked without the spec or produced drift the spec does not declare.
- README governance CI is absent or failing.

## Prohibitions
- Do not free-write or patch `README.md`.
- Do not vendor `readme-spec-engine` into the repository.
- Do not bypass enforcement by skipping README lint/governance checks.

## Rationale
Spec-first README generation keeps narratives auditable and reproducible.
Separating generation (external) from enforcement (this framework) avoids drift and hidden edits while keeping CI deterministic.
