# Skills

Skills are deterministic, stateless tool packages that execute without any LLM present. Agents/LLMs select and parameterize Skills; execution happens via the Skill’s declared runtime command with schema-defined JSON stdin/stdout.

Authoritative design: `docs/skills/skill-library-v1.md` (spec: `specs/skill-library-v1.md`).

## Create a Skill
1. Copy `skills/_template/` to `skills/<skill-slug>/`.
2. Update `skill.yaml` (`id`, `name`, `version`, `governance.specId`, access declarations).
3. Implement `impl/run.(py|js|sh)` with deterministic behavior (no prompts, no network unless approved).
4. Add fixtures and offline tests under `tests/` and `fixtures/`.

Optional scaffold helper (creates a new Skill directory + Spec stub):
- `scripts/skillctl scaffold <skill.id> <skill-slug>`

## Validate a Skill
- Validate the contract against `skills/_schema/skill.schema.json`.
- Validate input/output JSON against the Skill’s `schemas/input.schema.json` and `schemas/output.schema.json`.

Practical CLI (see `scripts/skillctl`):
- `scripts/setup-skillctl-venv.sh`
- `scripts/skillctl validate --all`
- `scripts/skillctl run <skill.id> --input input.json`
