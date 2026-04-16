# Stack Profile: Cloudflare Workers

Use this profile for Cloudflare Workers (edge). Pair it with the core governance rules in `AGENTS.md`.

## Runtime & Tooling
- JavaScript/TypeScript on Workers runtime; package manager per lockfile.
- Tooling: `wrangler` CLI; bundler (esbuild/Miniflare) per repo.
- Lint/format: ESLint/Prettier as configured.

## Project Layout
- `src/` for worker code; `wrangler.toml` for config; worker build output under `dist/`/`.wrangler` (ignored).

## Development Commands
- `npm install`
- `npm run dev` or `wrangler dev`
- `npm run build`
- `npm run lint`
- `npm run test` if configured

## Style & Naming
- Use TypeScript when available; keep handlers small and stateless.
- Avoid `console.log` spam in commits; prefer structured logs if supported.

## Testing Guidance
- Use Miniflare/worker-mocks for local tests; avoid hitting live services.
- Mock KV/durable objects/DO bindings in tests.

## Configuration & Ops
- Manage secrets via `wrangler secret`/environment variables; do not commit them.
- Document deploy command (`wrangler publish`) and environments.
