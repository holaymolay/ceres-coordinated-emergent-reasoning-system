# Stack Profile: Desktop (Electron / Tauri)

Use this profile for desktop apps built with Electron or Tauri. Pair it with the core governance rules in `AGENTS.md`.

## Runtime & Tooling
- Node.js 20 LTS; package manager per lockfile.
- Framework: Electron (JS/TS) or Tauri (Rust backend + JS/TS frontend).
- Lint/format: ESLint/Prettier for frontend; `cargo fmt`/`clippy` for Tauri Rust side.
- Testing: Jest/Vitest/RTL for frontend; `cargo test` for Tauri backend; E2E via Playwright/Spectron-like tools if configured.

## Project Layout
- Electron: `src/` for main/renderer; build artifacts under `dist/` or `out/`.
- Tauri: `src-tauri/` for Rust, `src/` for frontend; artifacts under `src-tauri/target/` and frontend `dist/`.

## Development Commands
- `npm install`
- Electron: `npm run dev` / `npm run build`.
- Tauri: `npm run tauri dev` / `npm run tauri build` (or `pnpm`/`yarn` equivalents).
- Lint/test per frontend choice; Tauri Rust: `cargo fmt`, `cargo clippy`, `cargo test`.

## Style & Naming
- Follow chosen frontend style guides; use structured logging; avoid stray `console.log`.
- For Tauri, keep Rust naming conventions and avoid `unwrap` in production paths.

## Testing Guidance
- Unit test UI logic; mock IPC/native bridges.
- For E2E, use Playwright/Cypress against built app where configured; keep tests deterministic.

## Configuration & Ops
- Manage secrets via env/build-time config; do not bundle secrets in binaries.
- Keep signing keys/certificates out of VCS; handle code signing via CI secrets.
