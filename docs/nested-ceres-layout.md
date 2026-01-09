# Nested CERES Layout and Bootstrap Plan
Status: Draft implementation plan for nesting CERES under `.ceres/` without loss of functionality.

## Goals
- Minimize visible footprint in user projects while retaining the full CERES stack.
- Keep governance immutable and pinned via `.ceres/core/`.
- Keep per-project artifacts in `.ceres/workspace/`.
- Avoid runtime behavior changes when the layer is absent or disabled; preserve backward compatibility with legacy root paths.

## Target Directory Structure
```
.ceres/
  core/              # pinned submodule of the CERES hub; governed via core.lock
  core.lock          # records tag/commit of core submodule
  workspace/         # per-project artifacts (authoritative when present)
    todo-inbox.md
    todo.md
    completed.md
    memory.md
    handover.md
    gap-ledger.json
    objective-contract.json
    prompts/
    specs/elicitation/
    memory/records/
    logs/events.jsonl
    synchronizations/
    modes_settings_profiles.json
    concepts/              # optional, project-owned concepts
  components/        # clones from repos.yaml (governance-orchestrator, etc.)
  bin/               # wrappers/shims for core scripts (preflight, start-session, export-handover, etc.)
```

## Defaults and Detection
- Default roots: `CERES_HOME=.ceres` and `CERES_WORKSPACE=.ceres/workspace` when present; otherwise fall back to legacy root files.
- Tooling behavior:
  - If `.ceres/workspace` exists, scripts resolve artifacts there first.
  - If absent, scripts use legacy root artifacts (backward compatibility).
  - Environment overrides (`CERES_HOME`, `CERES_WORKSPACE`) remain supported.
- Root loader: minimal `PROMPTLOADER.md` at project root instructs agents to load `.ceres/core/CONSTITUTION.md` and use `.ceres/workspace` as the artifact root.

## Bootstrap Flow (script outline)
Script: `scripts/bootstrap-workspace.sh`
- Inputs: optional `--core-ref <tag|commit>`, `--components` (bool), `--workspace <path>` (default `.ceres/workspace`).
- Steps:
  1) Create `.ceres/` if missing; initialize `core/` as submodule at ref; write `core.lock`.
  2) Copy workspace templates into `.ceres/workspace/` (todo artifacts, gap/objective, elicitation seed, memory scaffold, logs/).
  3) Optionally clone components from `repos.yaml` into `.ceres/components/` (reuse existing `scripts/clone-components.sh` with path override).
  4) Install wrappers into `.ceres/bin/` that delegate to `core/scripts/*` with workspace-aware defaults.
  5) Print next steps and active paths for transparency.
- Idempotency: safe re-run; skip existing files; do not overwrite submodule ref unless `--force` is provided.

## Wrapper Shims (`.ceres/bin/`)
- Provide thin entrypoints (bash/python) that:
  - Set `CERES_HOME`/`CERES_WORKSPACE` to `.ceres/`/`.ceres/workspace` if not already set.
  - Call corresponding `core/scripts/*` (e.g., `preflight.sh`, `start-session.sh`, `export-handover.py`).
  - Respect legacy behavior when `.ceres/` is missing.
- Installation: written by bootstrap script; cross-platform (POSIX sh) preferred.

## Migration and Back-Compat
- Detection order: `.ceres/workspace` → legacy root.
- No changes to governance documents; submodule keeps authority canonical.
- Existing repos can opt in by running bootstrap; legacy scripts keep working until migration is complete.
- Observability/Pattern recall: continue to store under `.ceres/workspace/logs/` (or `.ceres/patterns/` if observability namespace exists); removal must not affect execution.

## Acceptance and Tests (paper plan)
- Behavior parity: running preflight/plan/execute with `.ceres/` disabled vs enabled yields identical task ordering and outputs.
- Removal proof: deleting `.ceres/` causes scripts to fall back to legacy root without error.
- Wrapper validation: `.ceres/bin/preflight --mode execute` resolves `.ceres/workspace` by default; environment overrides still honored.
- Core pinning: `core.lock` matches submodule ref; validation script checks for drift.
- Footprint check: project root contains only `PROMPTLOADER.md` (and optional `.ceres/`); no other CERES files leak into root.
