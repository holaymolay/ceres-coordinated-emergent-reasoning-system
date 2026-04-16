# Stack Profile: Next.js (React/TypeScript)

Use this profile for React apps built with Next.js. Pair it with the core governance rules in `AGENTS.md`.

## Runtime & Tooling
- Node.js 20 LTS (align with `package.json` engines).
- Package manager: follow the lockfile (npm/pnpm/yarn).
- Framework: Next.js (App Router or Pages—check repo).
- Lint/format: `next lint` (ESLint) and Prettier if configured.
- Type checking: `next lint` (with types) or `tsc --noEmit` if present.
- Testing: Jest/Vitest with React Testing Library; Playwright/Cypress for E2E when present.

## Project Layout
- `app/` or `pages/` for routes; `components/`, `lib/`, `styles/`, `public/`.
- `.next/` is build output (ignored); env files `.env.local` etc. not committed.

## Development Commands
- `npm install`
- `npm run dev`
- `npm run build` / `npm start` (or `next start`)
- `npm run lint` (or `next lint`)
- `npm run test` (unit) / `npm run test:e2e` (if defined)
- `npm run typecheck` when present

## Style & Naming
- Use TypeScript (`.ts/.tsx`); components PascalCase; hooks `useX`.
- Follow project ESLint/Prettier rules; avoid stray `console.log` in committed code.

## Testing Guidance
- Co-locate tests near components/pages; mock network calls; avoid hitting live APIs.
- For App Router, test server components separately from client components where practical.

## Configuration & Ops
- Env via `.env.local`/`.env.<env>`; never commit secrets.
- Analyze bundle only in authorized contexts (`next build` + `next analyze` if enabled).
- Run `npm audit` or org security scans; document waivers.
