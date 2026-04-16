# Stack Profile: Rust

Use this profile for Rust services, CLIs, or libraries. Pair it with the core governance rules in `AGENTS.md`.

## Runtime & Tooling
- Rust stable via `rustup`; pin toolchain in `rust-toolchain.toml` when needed.
- Package manager/build tool: Cargo.
- Linting: `cargo clippy --all-targets --all-features`.
- Formatting: `cargo fmt`.
- Testing: `cargo test`; add `--all-features` when appropriate.
- Security/audit: `cargo audit`; optional `cargo deny` if configured.

## Project Layout
- Standard Cargo layout with `src/`, `tests/`, `examples/` as needed.
- Use workspaces for multi-crate repos; keep shared deps in workspace `Cargo.toml`.
- Keep build artifacts in `target/` (ignored).

## Development Commands
- `cargo fmt` — format.
- `cargo clippy --all-targets --all-features` — lint.
- `cargo test --all-features` — tests; add `-- --nocapture` for verbose output.
- `cargo build` or `cargo run` — build/run binaries.
- `cargo audit` — vulnerability scan (requires `cargo-audit` installed).

## Style & Naming
- Follow Rust naming: `snake_case` for functions/vars, `CamelCase` for types/traits, `SCREAMING_SNAKE_CASE` for consts/statics.
- Prefer `?` for error handling; avoid `unwrap`/`expect` in production paths.
- Use structured logging crates (`tracing`, `log`+backend) per project standard.

## Testing Guidance
- Unit tests inline with modules using `#[cfg(test)]`; integration tests under `tests/`.
- Use property-based testing (`proptest`) or snapshot testing where useful.
- Avoid network/filesystem side effects in unit tests; gate integration tests with features or env flags.

## Configuration & Ops
- Load config via env vars or files (e.g., `config` crate); never commit secrets.
- Pin Rust/Cargo versions in CI; keep lockfile (`Cargo.lock`) committed for binaries.
- For performance-sensitive code, include benches under `benches/` and run `cargo bench` when relevant.
