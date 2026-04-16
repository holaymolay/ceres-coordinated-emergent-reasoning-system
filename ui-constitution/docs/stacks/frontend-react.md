# Stack Profile: Frontend (React/TypeScript)

Use this profile for React + TypeScript frontends (Vite or Next.js). Pair it with the core governance rules in `AGENTS.md`.

## Runtime & Tooling
- Node.js 20 LTS (align with project engines field).
- Package manager: npm (or the project’s choice: pnpm/yarn—match the lockfile).
- Bundler: Vite or framework build (e.g., `next build`); adjust commands per app.
- Linting/formatting: ESLint + Prettier; TypeScript via `tsc --noEmit` or `next lint`.
- Testing: Vitest/Jest with React Testing Library; Playwright/Cypress for E2E when present.

## Project Layout
- `src/` holds app code; co-locate components, hooks, and tests (`__tests__` or `*.test.tsx`).
- `public/` (or `static/`) for assets; `scripts/` for tooling helpers.
- Keep build artifacts in `dist/` or `.next/` and out of VCS.

## Development Commands (baseline)
- `npm install` — install deps.
- `npm run dev` — start dev server.
- `npm run build` — production build.
- `npm run lint` — ESLint; add `npm run format` for Prettier or `npm run lint -- --fix` where configured.
- `npm run test` — unit tests; add `npm run test -- --coverage` as needed.
- `npm run typecheck` — TypeScript compile checks (or `next lint`/`next check` for Next.js).

## Style & Naming
- Use TypeScript (`.ts/.tsx`) where possible; enforce strict mode if enabled.
- Components PascalCase; hooks `useSomething`; files kebab- or camel-case per project convention.
- Prefer project logging utilities; avoid stray `console.log` in committed code.

## Testing Guidance
- Co-locate component tests next to components; use RTL for behavior-focused tests.
- Mock network calls; avoid hitting live services in unit tests.
- Mark E2E/integration tests separately to control runtime.

## Configuration & Ops
- Manage env vars via `.env*` files with safe defaults; never commit secrets.
- Align ESLint/Prettier/TypeScript versions with CI; update configs in lockstep.
- Run dependency audits (`npm audit` or stack-specific) and document waivers when necessary.
