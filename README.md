# CERES README Spec Engine
Part of the CERES (Coordinated Emergent Reasoning System). Umbrella repo: [CERES](https://github.com/holaymolay/ceres-coordinated-emergent-reasoning-system).
**Hub entry:** Load CERES via the umbrella `PROMPTLOADER.md` + `CONSTITUTION.md` (hub repo) and use hub todo templates/init script when bootstrapping; this component stays independent and is pulled via hub clone/run scripts.




## Why This Exists

Deterministic spec-to-artifact README generator and validator driven by explicit requirements.

## Audience

**Include**
- Repo maintainers who want README quality tied to explicit specs.
- Agents or scripts that need deterministic README generation.

**Exclude**
- Teams looking for marketing copy generation.
- Repos that want enforcement baked into the generator.

## Problem

README quality is often treated as subjective, making governance inconsistent and hard to audit. Without explicit structure, intent, and constraints, README changes drift and enforcement becomes ad hoc.

## Solution

readme-spec-engine converts explicit specs plus repo metadata into a deterministic README artifact and validates it against declared structure, audience, and constraints; enforcement and policy decisions live elsewhere. Workflow baseline snapshot: ai_workflow_revisions/rev_001_current (local).

## Outcomes

Expected outcomes:

- Generate README.md deterministically from README_SPEC.yaml.
- Validate README.md against declared structure, audience, and constraints.
- Produce a semantic diff between current and regenerated README.
- Keep README rules inspectable in YAML.

## Quick Start

Run these steps:

1. python -m venv .venv && source .venv/bin/activate
2. pip install -r requirements.txt
3. python src/generate_readme.py --spec README_SPEC.yaml --output README.md
4. python src/validate_readme.py --spec README_SPEC.yaml --readme README.md
5. python src/diff_readme.py --spec README_SPEC.yaml --readme README.md

## Repository Map

| Path | Description | Exists |
| --- | --- | --- |
| README_SPEC.yaml | Authoritative input spec for README generation. | yes |
| spec/ | YAML rules for sections, validation, and tone. | yes |
| src/ | CLI scripts for generate, validate, and diff. | yes |
| examples/ | Minimal and advanced spec examples. | yes |
| CLI.md | CLI usage and flags. | yes |

## Non-Goals

This tool explicitly avoids:

- Not a linter for arbitrary README content.
- Not marketing automation or copywriting.
- Not an enforcement mechanism; enforcement happens elsewhere.
- Not tied to any single repository's conventions.

## Constraints

Hard constraints:

- Max length: 5200 chars
- Banned terms: magic, automagic
- Tone profile: neutral
## Hub schemas
- Objective Contract, Gap Ledger, Task Plan, Completed entry, and Prompt Debug Report schemas live in the CERES hub `schemas/`. Consume them when generating/validating specs/README artifacts.

## Hub schema sync
- Use hub `scripts/sync-schemas.sh <target-repo>` to copy Objective Contract, Gap Ledger, Task Plan, Completed entry, Prompt Debug Report schemas into this repo when needed.

## Observability (local)
- Use  to emit stage events via hub .
