# Stack Profile: Elixir / Phoenix

Use this profile for Elixir services and Phoenix apps. Pair it with the core governance rules in `AGENTS.md`.

## Runtime & Tooling
- Elixir/Erlang versions per `.tool-versions` or `mix.exs`; use `asdf` to match.
- Dependency/build tool: `mix`.
- Lint/format: `mix format`; `mix credo` if configured.
- Testing: `mix test`.

## Project Layout
- Standard Phoenix layout with `lib/`, `test/`, `config/`, `assets/` (if front-end), `priv/`.
- Generated artifacts under `_build/` (ignored).

## Development Commands
- `mix deps.get`
- `mix compile`
- `mix test`
- `mix format`
- `mix credo` (if enabled)
- `mix phx.server` to run app

## Style & Naming
- Follow Elixir style; prefer immutable data and pipelines.
- Use `Logger` for logging; avoid `IO.inspect` in committed code.

## Testing Guidance
- Use ExUnit; keep tests isolated; mock external services with Mox when needed.
- Keep data factories/fixtures tidy and deterministic.

## Configuration & Ops
- Use `config/*.exs` with runtime config; keep secrets in env vars.
- Run `mix deps.audit` or equivalent for security; document waivers.
