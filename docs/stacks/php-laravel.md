# Stack Profile: PHP / Laravel

Use this profile for Laravel applications. Pair it with the core governance rules in `AGENTS.md`.

## Runtime & Tooling
- PHP 8.2+ (match project requirement); Composer for dependency management.
- Framework: Laravel; Artisan CLI for workflows.
- Lint/format: `phpcs`/`phpcbf` or `pint` per project config.
- Testing: `phpunit` or `artisan test`.

## Project Layout
- Standard Laravel structure with `app/`, `routes/`, `config/`, `database/`, `resources/`, `public/`.
- Environment config via `.env` (never commit secrets); cache config/routes/views for prod.
- Storage artifacts under `storage/` (gitignored); vendor deps under `vendor/`.

## Development Commands
- `composer install` — install deps.
- `php artisan serve` — run dev server.
- `php artisan migrate` — apply migrations; `php artisan db:seed` for seeds.
- `php artisan test` (or `vendor/bin/phpunit`) — run tests; add `--coverage` if configured.
- `./vendor/bin/pint` or `phpcbf` — format; `phpcs` to lint.

## Style & Naming
- Follow PSR-12; use Laravel naming conventions for controllers/models/migrations.
- Prefer dependency injection; avoid facades in domain logic where testability matters.
- Use Laravel logging (`Log` facade or PSR logger); avoid `var_dump/print_r` in committed code.

## Testing Guidance
- Place tests in `tests/Feature` and `tests/Unit`; use model factories and database refresh traits judiciously.
- Mock external services; avoid hitting live APIs.
- Keep migration/seeding repeatable; isolate filesystem/network side effects.

## Configuration & Ops
- Manage env vars via `.env` with `.env.example` updates; never commit real secrets.
- Cache config/routes in production (`php artisan config:cache`, `route:cache`).
- Run `composer audit` (or `symfony security:check`) if available; document waivers.
