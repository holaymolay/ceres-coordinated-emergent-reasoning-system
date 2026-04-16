# Stack Profile: R / Tidyverse

Use this profile for R analytics/reporting work. Pair it with the core governance rules in `AGENTS.md`.

## Runtime & Tooling
- R (match project version); package management via `renv` or `pak` preferred; otherwise `install.packages`.
- Style: `styler`/`lintr` per project config.
- Testing: `testthat`.

## Project Layout
- `R/` for functions; `tests/testthat/` for tests; `data/` for raw/processed (gitignored unless small fixtures); `scripts/` for ad-hoc runs.
- Avoid keeping large artifacts in repo; use `.gitignore`.

## Development Commands
- `renv::restore()` (or `pak::pkg_install`) to install deps.
- `lintr::lint_dir()` or project lint command.
- `styler::style_dir()` for formatting when appropriate.
- `devtools::test()` / `testthat::test_dir()` for tests.

## Style & Naming
- Follow tidyverse style: snake_case objects, clear function names, pipe-friendly APIs.
- Prefer `tibble`/`dplyr` semantics; avoid side effects in functions.

## Testing Guidance
- Use `testthat`; keep fixtures small; mock IO/network.
- For notebooks/RMarkdown, keep reproducible chunks and minimal cached outputs.

## Configuration & Ops
- Manage secrets via `.Renviron` or env vars; never commit real creds.
- Use `renv` lockfiles for reproducibility; run `renv::snapshot()` after changes.
