# Stack Profile: Django / Django REST Framework

Use this profile for Django apps and APIs (DRF). Pair it with the core governance rules in `AGENTS.md`.

## Runtime & Tooling
- Python 3.11+; use `python -m venv .venv`.
- Dependency management: `pip`/`pip-compile`/`poetry` per repo.
- Lint/format: `ruff`/`black`; type checks with `mypy` if enabled.
- Testing: `pytest` (preferred) or `python manage.py test`.

## Project Layout
- Django project folder with `settings.py`/`urls.py`; apps under `apps/` or root.
- Templates/static under `templates/` and `static/`; DRF serializers/views under app structure.
- Keep `media/`/`staticfiles/` outputs out of VCS.

## Development Commands
- `python -m venv .venv && source .venv/bin/activate`
- `pip install -r requirements.txt` (plus `-r requirements-dev.txt` if present)
- `python manage.py migrate`
- `python manage.py runserver`
- `ruff check .` / `black .`
- `pytest` (or `python manage.py test`)
- `mypy` when enabled

## Style & Naming
- PEP 8 + type hints; explicit settings per environment; avoid hardcoded secrets.
- Use Django logging; avoid `print`.

## Testing Guidance
- Use pytest + pytest-django; factory_boy for data; mock external services.
- Keep tests isolated (transactional DB, no external I/O); use fixtures for auth/permissions.

## Configuration & Ops
- Env via `.env` and settings modules; never commit real secrets.
- Apply migrations via `manage.py migrate`; seed with management commands/fixtures when needed.
- Run `pip-audit`/`safety` as part of security checks.
