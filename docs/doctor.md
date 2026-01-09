# CERES Doctor (Read-Only)
Status: Governance definition for the project-scoped Doctor command.

## Purpose
- Provide a deterministic, read-only snapshot of workspace health and governance integrity.
- Feed Signals and Self-Audit with evidence (never decisions).
- Improve operator awareness without affecting execution.

## Authority & Scope
- Non-authoritative, informational only. Removal must not alter CERES behavior.
- Project-scoped: inspects the active workspace and core pinning only.
- Outputs evidence; does not gate, fix, migrate, or modify artifacts.

## Allowed Inputs
- Workspace resolution (paths, presence of `.ceres/workspace` or legacy root).
- Core pin integrity (`core.lock` vs submodule commit, when present).
- Wrapper parity (wrapper presence/executable; fallback available).
- Feature flags (read-only; e.g., pattern recall).
- Removal-proof invariants (ability to operate without `.ceres/`).

## Allowed Outputs
- Human-readable report (stdout).
- Optional machine-readable JSON (flags or file path).
- Optional forwarding to Signals (one-way) for visibility.

## Prohibitions
- No auto-fix, no migrations, no writebacks beyond optional append-only signal emission.
- No enforcement or gating (exit code should reflect tool health, not governance verdicts).
- No implicit consumption by Planner/Execution; any use must be explicit.
- No ranking/scoring/recommendation of actions.

## Explicit Non-Checks (will never perform)
- Will not modify git state, run migrations, or change mode/profile settings.
- Will not reorder tasks, rewrite prompts/specs, or adjust governance artifacts.
- Will not schedule or trigger audits; emits visibility only.
