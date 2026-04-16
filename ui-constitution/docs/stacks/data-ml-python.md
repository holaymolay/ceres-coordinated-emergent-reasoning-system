# Stack Profile: Data/ML (Python)

Use this profile for data science and ML workflows in Python. Pair it with the core governance rules in `AGENTS.md`.

## Runtime & Tooling
- Python 3.11+ (match project requirement); use `python -m venv .venv` and activate before installs.
- Dependency management: `pip` with pinned `requirements.txt`/`requirements-dev.txt` or `pip-tools` (`pip-compile`/`pip-sync`); optionally `poetry`/`uv` if the project standardizes on them.
- Lint/format: `ruff` (lint/format) and/or `black`.
- Type checking: `mypy` when types are adopted.
- Testing: `pytest` with coverage (`--cov`).
- Notebooks: prefer `.ipynb` kept minimal; mirror logic into testable modules.

## Project Layout
- `src/` or package folder for reusable code; `notebooks/` for experiments; `data/` for raw/processed artifacts (gitignored).
- `tests/` mirrors package structure; fixtures under `tests/fixtures/`.
- `models/` or `artifacts/` for serialized models; keep out of VCS unless small/test assets.

## Development Commands (baseline)
- `python -m venv .venv && source .venv/bin/activate`
- `pip install -r requirements.txt` (add `-r requirements-dev.txt` for tooling) or `pip-sync` if using pip-tools.
- `ruff check .` / `ruff format .` (or `black .`)
- `pytest --cov`
- `mypy src tests` when types are present.

## Style & Naming
- PEP 8; docstrings for public functions/classes; prefer type hints in shared libraries.
- Avoid notebook-only logic; promote reusable code into modules.
- Logging via stdlib `logging`; avoid `print` for pipelines.

## Testing Guidance
- Unit-test feature engineering/model code; use deterministic seeds.
- Mock IO/external services; avoid live network in unit tests.
- For notebooks, add smoke tests that import and run key functions/scripts.

## Configuration & Ops
- Manage secrets via env vars or secret managers; never store creds in notebooks.
- Track data/model versions with checksums or DVC if adopted; document storage locations.
- Run vulnerability scans (`pip-audit` or org standard); pin versions for reproducibility.
