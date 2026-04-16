# Stack Profile: Julia

Use this profile for Julia projects (scientific/ML). Pair it with the core governance rules in `AGENTS.md`.

## Runtime & Tooling
- Julia (match project version); use `Pkg` for dependencies with `Project.toml`/`Manifest.toml`.
- Formatter: `JuliaFormatter`; linting via `StaticLint`/`Lint` if configured.
- Testing: `Pkg.test()`.

## Project Layout
- `src/` for code; `test/` for tests; `scripts/` for CLIs; `data/` gitignored unless fixtures.

## Development Commands
- `julia --project -e 'using Pkg; Pkg.instantiate()'`
- `julia --project -e 'using Pkg; Pkg.test()'`
- `julia --project -e 'using JuliaFormatter; format(".")'` when enabled.

## Style & Naming
- Follow Julia style: `snake_case` for vars/functions, `CamelCase` for modules/types.
- Prefer multiple dispatch idioms; avoid global mutable state.

## Testing Guidance
- Keep tests in `test/runtests.jl` and helpers in `test/` modules; mock IO/network.
- Seed randomness for reproducibility.

## Configuration & Ops
- Manage secrets via env vars; avoid hardcoding paths.
- Commit `Project.toml`/`Manifest.toml` for reproducibility; pin Julia version in CI.
