# Python Promotion Record

## Scope
This document records controlled promotions of Python fallbacks to primary execution paths.

## Current Promotion
- **Promoted script**: `scripts/preflight.py`
- **Primary wrapper**: `scripts/preflight.sh` now runs Python first and falls back to shell only on runtime failure or missing Python.
- **Evidence**: `docs/parity-verification.md` (Prompt 10 checklist).

## Rollback Instructions
To rollback this promotion in a single commit:
1. Edit `scripts/preflight.sh` and remove the Python‑primary block at the top.
2. Replace it with the prior fallback pattern:
   - Only run Python if available; on failure, continue with shell.
3. Commit the change with a message like: "Rollback preflight python promotion".

Shell logic must remain intact in all cases.
