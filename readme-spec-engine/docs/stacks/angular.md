# Stack Profile: Angular

Use this profile for Angular SPAs. Pair it with the core governance rules in `AGENTS.md`.

## Runtime & Tooling
- Node.js 20 LTS; package manager per lockfile (npm/pnpm/yarn).
- CLI: Angular CLI (`ng`).
- Lint/format: ESLint + Prettier (or `ng lint` defaults).
- Testing: `ng test` (Karma/Jasmine) or Jest if configured; E2E via Cypress/Playwright.

## Project Layout
- `src/` with `app/` modules/components/services; assets under `src/assets`; environment files under `src/environments`.
- Build output in `dist/` (ignored).

## Development Commands
- `npm install`
- `npm run start` or `ng serve`
- `npm run build` or `ng build`
- `npm run lint` / `ng lint`
- `npm run test` / `ng test`
- `npm run e2e` if configured

## Style & Naming
- Use TypeScript; components/services/modules PascalCase; selectors kebab-case.
- Follow Angular style guide; use `HttpClient` and dependency injection.

## Testing Guidance
- Use TestBed for components/services; mock HTTP with `HttpTestingController`.
- Keep E2E gated; avoid hitting live APIs.

## Configuration & Ops
- Env via `environment.ts` files; never commit secrets.
- Prefer strict mode; watch bundle size with `ng build --configuration production`.
