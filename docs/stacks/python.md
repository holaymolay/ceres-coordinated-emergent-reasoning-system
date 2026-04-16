# Stack Profile: Python

Use this profile for Python services and CLIs. Pair it with the core governance rules in `AGENTS.md`.

## Runtime & Tooling
- Python 3.11 (adjust per project requirements).
- Package management: `python -m venv .venv` for virtualenv; activate before installing.
- Dependency install: `pip install -r requirements.txt` (and `requirements-dev.txt` when present).
- Preferred formatters/linters: `black`, `ruff`, optional type checks via `mypy`.
- Testing: `pytest` with coverage (`pytest --cov`).

## Project Layout
- `src/` (or package-named folder) holds application code; avoid flat module sprawl.
- `tests/` mirrors the package structure; use `test_*.py` or `*_test.py`.
- Keep CLI entrypoints under `scripts/` or as console scripts in `pyproject.toml`.

## Development Commands (baseline)
- `python -m venv .venv && source .venv/bin/activate` — create/activate env.
- `pip install -r requirements.txt` — install runtime deps; add `-r requirements-dev.txt` for tooling.
- `ruff check .` — lint; `ruff format .` or `black .` — format.
- `pytest` — run tests; add `--cov` flags to enforce coverage thresholds.
- `mypy src tests` — optional static typing when project adopts type hints.

## Style & Naming
- Follow PEP 8 conventions; format with Black/Ruff to keep diffs clean.
- Use `snake_case` for modules/functions/variables; `PascalCase` for classes.
- Prefer stdlib `logging` for observability; avoid bare `print` in production code.

## Configuration & Ops
- Load environment variables via `.env` files or platform secrets; never commit real secrets.
- Pin dependencies where stability matters; run `pip-audit` (or equivalent) for vulnerability checks.
- Capture migrations/seed scripts under `scripts/` when the stack uses databases.

## Testing Guidance
- Keep fixtures close to tests (`tests/fixtures/` or alongside the test file).
- Mock external services; avoid network I/O in unit tests unless explicitly marked/integrated.
- Ensure new modules carry direct test coverage; gate merges on coverage deltas when feasible.
