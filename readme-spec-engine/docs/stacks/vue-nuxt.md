# Stack Profile: Vue / Nuxt

Use this profile for Vue apps and Nuxt SSR. Pair it with the core governance rules in `AGENTS.md`.

## Runtime & Tooling
- Node.js 20 LTS; package manager per lockfile.
- Framework: Vue 3 / Nuxt 3.
- Lint/format: ESLint + Prettier; TypeScript via `vue-tsc` when enabled.
- Testing: Vitest/Jest + Vue Testing Library; Playwright/Cypress for E2E when present.

## Project Layout
- Vue: `src/` with `components/`, `views/`, `router/`, `store/`.
- Nuxt: `pages/`, `components/`, `composables/`, `plugins/`, `server/`; build output in `.nuxt/` and `dist/`.

## Development Commands
- `npm install`
- `npm run dev`
- `npm run build`
- `npm run lint`
- `npm run test` (unit) / E2E commands as defined
- `npm run typecheck` or `vue-tsc --noEmit` when configured

## Style & Naming
- Use `<script setup>` + TypeScript where available; components PascalCase.
- Follow ESLint/Prettier rules; avoid stray `console.log` in commits.

## Testing Guidance
- RTL for components; mock network; avoid hitting live APIs in unit tests.
- For Nuxt server routes, test server handlers separately if feasible.

## Configuration & Ops
- Env via `.env`/`.env.<mode>`; never commit secrets.
- Respect Nuxt nitro adapter when deploying; test `npm run preview` before release.
