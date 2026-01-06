# Non‑Promotion Guardrails

These guardrails define when NOT to promote a Python fallback to primary execution.

## Do NOT promote if any condition is true
- **Parity is incomplete**: checklist rows not fully executed or any fail case unresolved.
- **High coupling**: script touches multiple subsystems or cross‑component boundaries.
- **Non‑determinism**: outputs vary across identical inputs or environments.
- **Security sensitivity**: script handles credentials, secrets, or key material.
- **Complex external dependencies**: requires network calls, system tools, or non‑stdlib Python packages.
- **Low ROI**: portability gain is minimal relative to risk and maintenance cost.
- **Operational fragility**: frequent env‑specific failures or hard‑to‑reproduce bugs.

## Promotion Gate (Minimal)
Before any promotion:
- Parity checklist **passed**.
- Post‑promotion verification **passed** for the previous promotion.
- Clear rollback plan documented.

If any gate is not met, promotion is blocked.
