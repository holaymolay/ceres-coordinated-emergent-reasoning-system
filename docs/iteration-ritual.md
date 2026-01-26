# Hard Iteration Contract (Optional)

## Guarantees
- OFF by default; no background loops and no automatic runs.
- Single-step only: one selection per invocation.
- Deterministic selection: highest priority where passes=false, tie-break by id ascending.
- No governance authority: writes only to owned artifacts.
- Removable: deleting the tool and owned files does not change core CERES behavior.

## Owned Artifacts
- scripts/iteration/backlog.json
- scripts/iteration/progress.jsonl
- scripts/iteration/README.md

## Usage
Run one step:
```
python scripts/iteration/run.py
```

Optional flags:
- --backlog <path>
- --progress <path>
- --set-pass true|false
- --evidence-ref <string> (repeatable)
- --dry-run
- --show-order

## Uninstall
- Delete `scripts/iteration/`.
- No other files are required by core CERES.
