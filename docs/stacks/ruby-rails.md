# Stack Profile: Ruby on Rails

Use this profile for Rails apps. Pair it with the core governance rules in `AGENTS.md`.

## Runtime & Tooling
- Ruby version per `.ruby-version`; use `rbenv`/`asdf` to match.
- Dependency management: Bundler (`bundle install`).
- Lint/format: `rubocop` (and `rubocop -A` for autofix when allowed).
- Testing: `bundle exec rspec` or `rails test` depending on setup.

## Project Layout
- Standard Rails structure under `app/`, `config/`, `db/`, `lib/`, `test/` or `spec/`.
- Credentials/env via `config/credentials.*` or env vars; never commit real secrets.
- DB schema/migrations under `db/`; assets under `app/assets` or `app/javascript` (Webpacker/Vite).

## Development Commands
- `bundle install`
- `bin/rails db:prepare` (creates/migrates)
- `bin/rails server`
- `bundle exec rubocop`
- `bundle exec rspec` or `bin/rails test`

## Style & Naming
- Follow community/RuboCop rules; use snake_case file/class names aligned to module paths.
- Prefer `Rails.logger` over `puts`.

## Testing Guidance
- Use factories/fixtures; keep tests isolated; stub external services.
- For system tests, gate browser drivers appropriately.

## Configuration & Ops
- Manage secrets via Rails credentials or env; keep `config/master.key` out of VCS unless explicitly shared securely.
- Run `bundle exec bundler-audit` or org security scans; document waivers.
