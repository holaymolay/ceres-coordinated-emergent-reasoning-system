# Stack Profile: Deno / Fresh

Use this profile for Deno projects and Fresh apps. Pair it with the core governance rules in `AGENTS.md`.

## Runtime & Tooling
- Deno (match `deno --version`); uses built-in tooling (no npm unless using compat).
- Lint/format: `deno fmt`, `deno lint`.
- Testing: `deno test`.

## Project Layout
- Fresh: `routes/`, `islands/`, `components/`, `static/`; config in `fresh.config.ts`.
- General Deno: `src/`/`mod.ts`; deps via URL imports or `deno.json`.

## Development Commands
- `deno task dev` (Fresh) or `deno run`/`deno task <name>` per `deno.json`.
- `deno fmt`
- `deno lint`
- `deno test`

## Style & Naming
- Use TypeScript by default; keep imports pinned to versions.
- Avoid `console.log` noise; use loggers if added.

## Testing Guidance
- Use `deno test` with permissions scoped; mock fetch/network as needed.

## Configuration & Ops
- Manage env via `Deno.env` and `.env` support when enabled; avoid embedding secrets.
- Run with least privileges (`--allow-*`) and document required permissions.
