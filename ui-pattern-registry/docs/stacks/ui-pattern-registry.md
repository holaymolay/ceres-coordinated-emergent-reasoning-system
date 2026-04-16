# Stack Profile: UI Pattern Registry (Node.js Tooling)

Use this profile for the UI Pattern Registry repository. It is a data/validation toolkit (no runtime server) built with Node.js and npm.

## Runtime & Tooling
- Node.js 20 LTS
- Package manager: npm
- ESM JavaScript for scripts/tests; dependencies: `ajv`, `yaml`, `glob`
- Dev tools: ESLint (`eslint:recommended`), Node built-in test runner
- Logging: CLI output via `console` only (structured, concise); no runtime logging framework needed

## Project Layout
- `schemas/` — JSON Schemas for registry data
- `patterns/` — Pattern definitions grouped by category (layouts, compositions, interactions)
- `scripts/` — Validation and governance automation (JavaScript)
- `tests/` — Node tests and fixtures for validation tooling
- `docs/` — Project and governance documentation
- `ai_workflow_revisions/` — Local workflow snapshots (gitignored)
- `runs/` — Run records (JSONL) per task

## Development Commands
- `npm install` — install dependencies
- `npm run lint` — ESLint over scripts/tests
- `npm run validate` — Validate all pattern files against schemas
- `npm test` — Run lint + validate + Node tests (includes fixtures for failure cases)

## Style & Naming
- ESM modules with 2-space indentation and LF endings
- Filenames in kebab-case for scripts/tests (e.g., `validate-patterns.js`, `pattern-validation.test.js`)
- Prefer small, pure functions; avoid side effects outside CLI output
- Keep CLI output deterministic and machine-readable when feasible

## Testing Guidance
- Tests live under `tests/` using the Node test runner (`node --test`)
- Use fixtures in `tests/fixtures/` to cover valid/invalid pattern cases
- Ensure validation scripts return non-zero on failures and emit actionable error messages

## Configuration & Ops
- No runtime environment variables or secrets required
- Dependencies pinned via `package-lock.json`; audit with `npm audit` when dependency changes land
- CI: GitHub Actions workflow runs `npm ci`, `npm run lint`, `npm run validate`, and `npm test`
- Generated artifacts (coverage, node_modules) remain untracked; keep `.gitignore` updated accordingly
