# Stack Profile: SvelteKit

Use this profile for SvelteKit apps. Pair it with the core governance rules in `AGENTS.md`.

## Runtime & Tooling
- Node.js 20 LTS (match repo engines).
- Package manager: follow lockfile (npm/pnpm/yarn).
- Framework: SvelteKit.
- Lint/format: ESLint + Prettier (or `svelte-check` formatting); TypeScript via `svelte-check`.
- Testing: Vitest/Playwright per repo setup.

## Project Layout
- `src/routes/`, `src/lib/`, `static/`; build output in `.svelte-kit/` and `build/`.

## Development Commands
- `npm install`
- `npm run dev`
- `npm run build`
- `npm run lint` / `npm run check` (TypeScript+Svelte)
- `npm run test` / `npm run test:unit` / `npm run test:e2e` as defined

## Style & Naming
- Use TypeScript where enabled; components PascalCase; actions/hooks kebab/camel per project.
- Follow SvelteKit lint rules; avoid stray `console.log` in commits.

## Testing Guidance
- Use `svelte-testing-library`/RTL for components; mock fetch/network; keep E2E isolated.

## Configuration & Ops
- Env via `.env`/`.env.<mode>`; never commit secrets.
- Respect adapter choice (static/node/vercel); run adapter-specific previews when relevant.
