# Stack Profile: Node.js / Express

Use this profile when working on Node.js services built with Express. Pair it with the core governance rules in `AGENTS.md`.

## Runtime & Tooling
- Node.js 20 LTS (adjust only with explicit approval).
- Package manager: npm.
- Frameworks: Express + Handlebars (if present).
- Logging: prefer `pino` helpers over `console.log` in committed code.

## Project Layout
- `src/` holds application code with `server.js` (or equivalent) bootstrapping middleware, routes, and views.
- `src/config/` for configuration helpers; `src/middleware/` for HTTP middleware; `src/routes/` for handlers; `src/services/` for domain logic; `src/public/` for static assets.
- Persistent artifacts (e.g., SQLite db files, generated PDFs) live in `data/` (created automatically). Keep `data/` out of VCS.

## Development Commands
- `npm install` — install dependencies.
- `npm run dev` — start dev server with Nodemon and `NODE_ENV=development` for live reloads.
- `npm start` — launch the production server.
- `npm run lint` / `npm run lint:fix` — ESLint with Standard + Prettier; `:fix` auto-resolves style issues.
- `npm test` — Jest in-band using the Node environment; coverage written to `coverage/`. Add `-- --coverage` for explicit coverage runs.

## Style & Naming
- Standard JS + Prettier config (single quotes, no semicolons, ~100-character lines); `.editorconfig` enforces two-space indentation and LF endings.
- Filenames: kebab- or camel-case (e.g., `invoiceRoutes.js`, `generate-report.service.js`).
- Keep external libraries vendor-neutral; avoid patching deps.

## Testing Guidance
- Place tests under `tests/` ending with `.test.js` (`**/tests/**/*.test.js` picked up by Jest).
- Use SuperTest for HTTP assertions; keep fixtures alongside test files.
- Target coverage regressions explicitly; ensure new modules have direct test coverage.

## Configuration & Ops
- Environment variables load from `.env.<NODE_ENV>` falling back to `.env`. Document new keys with safe defaults.
- SQLite path defaults to `data/app.db`; add migrations/seed scripts under `scripts/` when needed.
- Run `npm audit` (or equivalent) as part of dependency hygiene; remediate or document risk waivers.
