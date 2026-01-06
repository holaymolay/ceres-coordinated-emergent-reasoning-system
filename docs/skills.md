# Skills Framework (CERES)

This defines a formal Skills model for CERES agents. Skills are reusable, stateless capabilities that extend agent behavior without bypassing governance, Concepts, or Synchronizations.

## Model

A Skill must declare:
- `name`
- `purpose`
- `inputs`
- `outputs`
- `constraints`
- `allowed_roles`
- `entrypoint`
- `type` (`analytical` or `transform`)

Schema: `schemas/skill.schema.json`
Registry: `skills/registry.yaml`

## Registry

The registry is a single YAML file listing available skills and metadata. It is machine‑readable and validated by the loader.

## Governance & Enforcement

- Skills are **read-only** or **pure transforms**.
- Skills do **not** write to Concepts, Synchronizations, or system state.
- Skills are invoked through the skill invoker, which:
  - Requires `role` authorization.
  - Requires an explicit `concept` scope.
  - Logs every invocation to `logs/skill-invocations.jsonl`.
  - Rejects multi-concept inputs and concept dependency declarations.
  - Validates `sync_dependencies` against `synchronizations/` when provided.

## Invocation

```bash
node skills/skill-invoker.js \
  --skill summarize-text \
  --role planner \
  --concept governance \
  --input '{"text":"Some long text..."}'
```

If a skill declares sync usage, pass `sync_dependencies` in the input payload; the invoker validates them against `synchronizations/`.

## Example Skills

- `summarize-text` (analytical, read-only)
- `normalize-keys` (transform, pure)

## Why This Is Safe

The skills framework enforces role authorization, explicit Concept scope, deterministic execution, and structured logging. It adds capability without weakening governance or crossing Concept boundaries.
