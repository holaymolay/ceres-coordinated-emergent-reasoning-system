# Stack Profile: WordPress

Use this profile for WordPress sites/plugins/themes. Pair it with the core governance rules in `AGENTS.md`.

## Runtime & Tooling
- PHP version per project (match host); Composer for deps when applicable.
- Lint/format: `phpcs`/`phpcbf` with WordPress ruleset; `pint` if preferred.
- Testing: `phpunit`/`wp scaffold plugin-tests` setup; integration tests via WP-CLI when configured.

## Project Layout
- Core + `wp-content/` with `themes/` and `plugins/`; custom code should live in theme/plugin directories, not core.
- Keep uploads and cache out of VCS; vendor deps under `vendor/` when used.

## Development Commands
- `composer install` (when using Composer).
- WP-CLI for local env/tasks: `wp server`, `wp plugin activate`, etc.
- `phpunit` / `wp scaffold plugin-tests` test runner; `npm run build` for block builds if using build tooling.
- `phpcs` / `phpcbf` or `pint` per project.

## Style & Naming
- Follow WordPress coding standards; prefix functions/classes to avoid collisions.
- Avoid editing core; use hooks/filters.
- Use WP logging mechanisms; avoid `var_dump/print_r` in committed code.

## Testing Guidance
- Prefer plugin/theme-level tests; mock external calls; use factories for DB fixtures.
- Gate integration tests that hit real DB/state.

## Configuration & Ops
- Manage secrets via `wp-config.php` env vars; never commit real creds.
- Document deployment steps (build assets, DB migrations if any, cache clear); avoid committing uploads.
