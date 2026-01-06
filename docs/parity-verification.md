# Parity Verification Checklist (Shell ↔ Python)

## Purpose
This checklist proves that Python fallback scripts behave identically to their shell counterparts. Passing this checklist is a hard gate before any Python promotion.

## Scope
Only shell scripts that currently have Python fallbacks:
- `scripts/preflight.sh` ↔ `scripts/preflight.py`
- `scripts/validate-arbitration-ci.sh` ↔ `scripts/validate-arbitration-ci.py`

Lifecycle/phase-gate scripts: none exist in the hub at this time.

## Parity Dimensions (All Required)
1. Exit Codes
   - Success, failure, early-exit/skip conditions must match.
2. Execution Order
   - Sub-steps occur in the same sequence.
3. Failure Modes
   - Same conditions fail/pass.
4. Output Semantics
   - Human-readable meaning matches.
   - stdout vs stderr usage is consistent.
5. Determinism
   - Same inputs produce identical outputs.
   - No environment-dependent variance.

## Verification Method
This checklist is designed for manual execution. A minimal comparison harness is available:

```bash
scripts/compare-shell-python.sh preflight --mode execute --prompt todo-inbox.md
scripts/compare-shell-python.sh validate-arbitration-ci
```

The harness runs both scripts, captures stdout/stderr and exit codes, and reports mismatches.

## Checklist: preflight.sh ↔ preflight.py

**Preconditions**
- Run from repo root.
- `prompt-debugger/cli.py` exists and is executable.
- `governance-orchestrator` is available via `scripts/run-component.sh`.

| Test Case | Setup / Input | Expected Outcome | Actual | Pass/Fail |
|---|---|---|---|---|
| Invalid mode | `--mode invalid` | Exit 1; stderr: "Invalid mode: invalid (expected plan or execute)" |  |  |
| Missing prompt file | `--prompt missing.md` | Exit 1; stderr: "Prompt file not found: …" |  |  |
| Missing objective contract | Provide valid prompt + report; remove `objective-contract.json` | Exit 1; stderr: "Objective Contract missing" |  |  |
| Missing gap ledger | Provide valid prompt + objective; remove `gap-ledger.json` | Exit 1; stderr: "Gap Ledger missing" |  |  |
| Gap ledger blocking in execute | `gap-ledger.json` contains unresolved blocking gap | Exit 1; stderr: "Blocking gaps unresolved" |  |  |
| Objective status invalid | Objective status != committed in execute | Exit 1; stderr: "Objective Contract status must be 'committed'" |  |  |
| Happy path (execute) | Valid prompt + objective + gap ledger | Exit 0; stdout: "Preflight checks passed (execute mode)." |  |  |

**Determinism Check**
- Run the same command twice; stdout/stderr and exit codes must match exactly.

## Checklist: validate-arbitration-ci.sh ↔ validate-arbitration-ci.py

**Preconditions**
- Run from repo root.
- `node` is available.
- `arbitration/arbitrator.js` exists.

| Test Case | Setup / Input | Expected Outcome | Actual | Pass/Fail |
|---|---|---|---|---|
| Missing arbitrator | Temporarily move `arbitration/arbitrator.js` | Exit 1; stderr: "Arbitration engine not found" |  |  |
| No planner outputs | Ensure no planner output directories | Exit 0; stderr includes "using fixture input"; stdout contains decision JSON |  |  |
| Invalid planner dir via env | `ARBITRATION_PLANNER_DIR=/bad/path` | Exit 1; stderr indicates invalid directory |  |  |
| Planner output missing files | Set env to dir missing one artifact | Exit 1; stderr indicates missing artifacts |  |  |
| Planner output invalid | Provide artifacts that fail validator | Exit 1; stderr shows validator errors |  |  |
| Happy path with planner output | Valid artifacts in a single dir | Exit 0; stdout decision JSON; determinism check passes |  |  |

**Determinism Check**
- Run both scripts twice against the same input; stdout/stderr and exit codes must match exactly.

## Promotion Readiness Criteria (Binary Gate)
Python fallbacks are eligible to become primary ONLY if all conditions are met:
- All checklist rows above are marked **Pass** for every script pair.
- Exit codes match for every test case.
- stdout/stderr semantics match for every test case.
- Determinism checks pass (identical outputs under identical inputs).
- No undefined behavior or environment-dependent variance is observed.

If any single check fails, promotion is **blocked**.

## Governance Fit
This checklist is a governance gate: it provides auditable proof of behavioral parity before any authority shift from shell to Python.
