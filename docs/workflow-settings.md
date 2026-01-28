# CERES Workflow Settings

This document defines macro-level workflow knobs for CERES and how to validate changes.

## File
- `ceres.workflow.yaml` (repo root or `.ceres/workspace/ceres.workflow.yaml` in nested layout)

## Macro Knobs
- auto_housekeeping: true | false
- auto_push: true | false
- announce_push: true | false

These are coarse-grained controls to shape routine workflow behavior. No fine-grained tuning without governance review.

## Safeguards
- Changes are validated and warnings are shown before apply.
- Warnings require explicit confirmation to proceed.
- Validation is deterministic and rule-based.

## Workflow (CLI)
1) Copy current workflow config to a proposed file:

```
cp ceres.workflow.yaml ceres.workflow.proposed.yaml
```

2) Edit `ceres.workflow.proposed.yaml`.
3) Validate and review warnings:

```
python scripts/workflow_guard.py --current ceres.workflow.yaml --proposed ceres.workflow.proposed.yaml
```

4) Apply with confirmation (warnings require explicit confirmation):

```
python scripts/workflow_guard.py --current ceres.workflow.yaml --proposed ceres.workflow.proposed.yaml --apply
```

Add `--confirm` to proceed non-interactively when warnings exist.
5) Optionally remove the proposed file after apply.

### Helper (recommended)
Use the helper to create the proposed file (if missing) and run validation:

```
python scripts/workflow_edit.py --open
```

Apply after review:

```
python scripts/workflow_edit.py --apply
```

## Notes
- Preflight runs the workflow guard in advisory mode (non-blocking).
- Housekeeping respects the workflow config by default.
