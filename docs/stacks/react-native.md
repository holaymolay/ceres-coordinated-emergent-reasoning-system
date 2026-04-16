# Stack Profile: React Native

Use this profile for React Native apps. Pair it with the core governance rules in `AGENTS.md`.

## Runtime & Tooling
- Node.js 20 LTS; package manager per lockfile.
- React Native CLI or Expo (check repo).
- Lint/format: ESLint + Prettier.
- TypeScript via `tsc --noEmit` if present.
- Testing: Jest + React Native Testing Library; Detox/E2E when configured.

## Project Layout
- `android/`, `ios/`, `app/` or `src/`; assets under `assets/`.
- Build artifacts under `android/app/build`, `ios/build`, etc. (ignored).

## Development Commands
- `npm install`
- `npm run start` (Metro)
- `npm run android` / `npm run ios` (or `expo start` workflows)
- `npm run lint`
- `npm run test`

## Style & Naming
- Components PascalCase; hooks `useX`; keep platform-specific files (`*.ios.tsx`, `*.android.tsx`) when needed.
- Avoid stray `console.log` in commits; use project logging utilities.

## Testing Guidance
- Use RTL for components; mock native modules and network requests.
- For Detox/E2E, gate runs because they require emulators/simulators.

## Configuration & Ops
- Manage env via `app.config.js`/`.env` and platform config; never commit secrets or signing keys.
- Keep `android/local.properties`, keystores, and `ios/*.xcworkspace` settings secure and out of VCS.
