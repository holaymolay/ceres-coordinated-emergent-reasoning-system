# CERES Macro Policy Settings

This document defines the macro-level policy knobs that are safe for human adjustment and provides the validation workflow.

## File
- `ceres.policy.yaml` (root)

## Macro Knobs
- rigor_level: low | standard | high
- autonomy_level: minimal | constrained | advanced
- risk_tolerance: low | medium | high
- execution_continuity: manual | auto-safe
- observability_depth: normal | verbose

These are coarse-grained controls; no fine-grained tuning should be added without governance review.

## Safeguards
- Changes are validated and warnings are shown before apply.
- Warnings require explicit confirmation to proceed.
- Validation is deterministic and rule-based.

## Workflow (CLI)
1) Copy current policy to a proposed file:

```
cp ceres.policy.yaml ceres.policy.proposed.yaml
```

2) Edit `ceres.policy.proposed.yaml`.
3) Validate and review warnings:

```
python scripts/policy_guard.py --current ceres.policy.yaml --proposed ceres.policy.proposed.yaml
```

4) Apply with confirmation (warnings require explicit confirmation):

```
python scripts/policy_guard.py --current ceres.policy.yaml --proposed ceres.policy.proposed.yaml --apply
```

Add `--confirm` to proceed non-interactively when warnings exist.
5) Optionally remove the proposed file after apply.

### Helper (recommended)
Use the helper to create the proposed file (if missing) and run validation:

```
python scripts/policy_edit.py --open
```

Apply after review:

```
python scripts/policy_edit.py --apply
```

## Minimal GUI Flow (Design)
- Present macro knobs as a small form (dropdowns only; no freeform tuning).
- "Validate" runs the policy guard in advisory mode and surfaces warnings.
- "Apply" requires explicit confirmation if warnings exist.
- Writes only to `ceres.policy.yaml`; no automatic execution or background effects.

## Notes
- Preflight runs the policy guard in advisory mode (non-blocking).
- This policy remains advisory until explicitly wired into enforcement gates.
- Guardrails are conservative by default and should err on safety.
