# Rigor CLI (Default-Off)

These commands are optional, default-off, and do not change core execution paths.

## Commands
- `python scripts/rigor.py verify --rigor rigor.json`
- `python scripts/rigor.py check-spec-map --rigor rigor.json --spec-clauses spec-clauses.json`
- `python scripts/rigor.py run-oracle --rigor rigor.json`
- `python scripts/rigor.py exploit-probe --rigor rigor.json`
- `python scripts/rigor.py nondeterminism-report --rigor rigor.json --task-meta task-meta.json`

Each command emits a JSON report to stdout (or `--out <path>`), and logs an advisory event via `scripts/log_event.py`.

## Inputs
- `rigor.json`: Rigor configuration matching `schemas/rigor.schema.json`.
- `spec-clauses.json`: JSON array of spec clause identifiers (or newline list).
- `task-meta.json`: JSON/YAML object with `networked: true|false`.

## Outputs
- Reports conform to `schemas/rigor-report.schema.json`.
- Events are type `rigor`, status `pass|fail|warn`, and include context.
