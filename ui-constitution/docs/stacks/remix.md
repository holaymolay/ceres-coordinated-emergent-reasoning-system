# Stack Profile: Remix (React)

Use this profile for Remix apps. Pair it with the core governance rules in `AGENTS.md`.

## Runtime & Tooling
- Node.js 20 LTS; package manager per lockfile.
- Framework: Remix (React).
- Lint/format: ESLint + Prettier; TypeScript via `tsc --noEmit` if configured.
- Testing: Vitest/Jest + RTL; Playwright for E2E when present.

## Project Layout
- `app/` for routes/components/loaders/actions; `public/` for static assets; build output under `build/`.

## Development Commands
- `npm install`
- `npm run dev`
- `npm run build`
- `npm run start`
- `npm run lint`
- `npm run test` (unit) / `npm run test:e2e` if defined
- `npm run typecheck` when present

## Style & Naming
- Use TypeScript; route modules PascalCase as needed; keep loaders/actions thin.
- Avoid stray `console.log` in commits.

## Testing Guidance
- Test loaders/actions with mocked fetch/request objects; mock network calls.
- Use RTL for components; gate Playwright E2E runs.

## Configuration & Ops
- Env via `.env`/`.env.<env>`; never commit secrets.
- Document deployment target (Node server, Cloudflare Workers, etc.) and adapter-specific commands.
