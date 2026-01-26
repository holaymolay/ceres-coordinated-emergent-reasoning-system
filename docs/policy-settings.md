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

## Workflow
1) Edit `ceres.policy.yaml` or create a proposed file.
2) Run the policy guard to validate and apply:

```
python scripts/policy_guard.py --current ceres.policy.yaml --proposed ceres.policy.proposed.yaml --apply
```

Add `--confirm` to proceed non-interactively when warnings exist.

## Notes
- This policy is advisory until explicitly wired into enforcement gates.
- Guardrails are conservative by default and should err on safety.
