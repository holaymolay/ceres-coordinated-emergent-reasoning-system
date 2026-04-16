# Stack Profile: FastAPI

Use this profile for FastAPI services. Pair it with the core governance rules in `AGENTS.md`.

## Runtime & Tooling
- Python 3.11+; `python -m venv .venv`.
- Dependency management: `pip`/`pip-compile`/`poetry` per repo.
- Lint/format: `ruff`/`black`; type checks with `mypy`.
- Testing: `pytest` with httpx/Starlette test client.

## Project Layout
- `app/` or `src/` for application code; routers under `api/` or `routes/`; models/schemas/services grouped by domain.
- `tests/` mirroring app layout; fixtures under `tests/fixtures/`.

## Development Commands
- `python -m venv .venv && source .venv/bin/activate`
- `pip install -r requirements.txt` (plus `-r requirements-dev.txt` if present)
- `uvicorn app.main:app --reload`
- `ruff check .` / `black .`
- `pytest --cov`
- `mypy app tests`

## Style & Naming
- Use pydantic models for request/response; keep pure domain logic separate from I/O.
- PEP 8 + type hints; prefer dependency injection via FastAPI `Depends`.

## Testing Guidance
- Use httpx/Starlette test client; mock external services; avoid hitting live APIs.
- Seed data via fixtures; keep DB interactions isolated/transactional.

## Configuration & Ops
- Env via `.env`/settings module; never commit secrets.
- Run security scans (`pip-audit`, dependency review); document waivers.
