# Post-Promotion Verification Checklist (Preflight)

## Purpose
Validate the real‑world behavior of the Python‑primary preflight after promotion. This is a time‑bound observation window, not a new gate.

## Scope
- Script: `scripts/preflight.py` (primary)
- Fallback: `scripts/preflight.sh` (only on Python runtime failure or missing Python)
- Duration: 1–2 weeks of normal usage

## What to Monitor (Required)
1. **Unexpected fallbacks**
   - Capture stderr on each preflight run.
   - Count any `WARN: ... fallback` occurrences.
   - Investigate cause and classify as:
     - Python runtime failure (traceback/module/syntax)
     - Missing python3
     - Other
2. **Divergent outputs**
   - Compare stdout/stderr between Python and shell for identical inputs when fallbacks occur.
   - Any mismatch is a regression and blocks further promotion.
3. **Environment‑specific issues**
   - Record OS, shell, and Python version when failures occur.
   - Note any reproducible environment patterns (e.g., missing `yaml` in Python).

## How to Capture Evidence (Manual)
- When running preflight, capture stderr:

```bash
scripts/preflight.sh --mode execute 2>> logs/preflight-run.log
```

- Scan for fallback usage:

```bash
rg "fallback" logs/preflight-run.log
```

- If a fallback occurs, re-run both paths with identical inputs:

```bash
scripts/compare-shell-python.sh preflight -- --mode execute
```

## Pass/Fail Criteria
- **Pass**: No unexpected fallbacks AND no output mismatches across the observation window.
- **Fail**: Any unexpected fallback without a clear Python runtime cause, or any mismatch in outputs/exit codes.

## Exit Decision
- If pass: eligible to consider *one* additional promotion later.
- If fail: freeze promotions until root cause is resolved and parity re‑verified.
