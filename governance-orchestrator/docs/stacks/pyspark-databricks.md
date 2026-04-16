# Stack Profile: PySpark / Databricks

Use this profile for Spark workloads (local or Databricks). Pair it with the core governance rules in `AGENTS.md`.

## Runtime & Tooling
- Python 3.11+ with PySpark version matching the cluster/runtime; manage env via `venv`/`conda`.
- Dependency management: `pip`/`pip-compile`/`poetry` per project; align with cluster libraries.
- Lint/format: `ruff`/`black`; type checks with `mypy` if enabled.
- Testing: `pytest` with Spark session fixtures.

## Project Layout
- `src/` or package folder for jobs/libraries; `jobs/` or `notebooks/` for entrypoints; `tests/` mirroring code; `conf/` for cluster/job configs.
- Keep large datasets out of repo; use sample fixtures under `tests/fixtures/`.

## Development Commands
- `python -m venv .venv && source .venv/bin/activate`
- `pip install -r requirements.txt` (and `-r requirements-dev.txt` if present)
- `pytest` (with Spark session fixture)
- `ruff check .` / `black .`
- `mypy src tests` when types are present

## Style & Naming
- PEP 8 + type hints where feasible; avoid hardcoded paths/bucket names.
- Use DataFrame APIs consistently; avoid UDFs unless necessary; prefer `pyspark.sql.functions`.

## Testing Guidance
- Use local Spark session fixture; keep datasets tiny; mock external systems.
- For notebooks, mirror core logic into tested modules.

## Configuration & Ops
- Parameterize jobs via configs/env; avoid committing secrets (use key vault/secrets scopes).
- Align Python and Spark versions with cluster runtime; document job submission commands (e.g., `databricks jobs run`, `spark-submit`).
