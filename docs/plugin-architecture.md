# CERES Plugin Architecture

Plugins extend CERES with optional, versioned capabilities without mutating Concepts or bypassing enforcement. They observe, analyze, and suggest only.

## Hook Lifecycle Diagram (Text)

```
[Planner] -> pre_planning -> [Plugins] -> plan -> post_planning -> [Plugins]
                                  |
                                  v
                          pre_arbitration -> [Plugins] -> arbitration -> post_arbitration -> [Plugins]

Observability-only hooks can run at any time without influencing execution.
```

## Plugin Model (Schema)

A plugin must declare:
- `name`
- `version`
- `purpose`
- `compatibility` (core_min/core_max)
- `hook_points`
- `constraints`
- `entrypoint`
- `type` (`analysis` or `suggestion`)

Schema: `schemas/plugin.schema.json`
Registry: `plugins/registry.yaml`

## Isolation & Governance Rules

- Plugins **never** mutate Concepts or Synchronizations.
- Plugins **never** decide, execute, or bypass enforcement.
- Plugins operate only on declared inputs and emit non-binding output.
- Plugin failures are logged but do not crash core execution.

## Data Contract for Plugin Runner

Invocation requires:
- `--hook` (hook point)
- `--role` (invoking agent role)
- `--concept` (active concept)
- `--input` (JSON payload)

The runner enforces:
- Explicit Concept scope
- Single-Concept inputs only
- Role authorization (if defined)

## Component Outline

- `plugins/registry.yaml`: plugin index and metadata
- `plugins/plugin-loader.js`: registry parser/validator
- `plugins/plugin-runner.js`: runner with governance checks + logging
- `plugins/examples/`: example plugins (analysis + suggestion)

## Why This Preserves CERES Guarantees

Plugins are opt-in, reversible, and read-only. The runner logs every invocation and treats outputs as advisory signals only, preventing implicit dependencies or hidden execution control.
