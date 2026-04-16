# Stack Profile: Go

Use this profile for Go services and CLIs. Pair it with the core governance rules in `AGENTS.md`.

## Runtime & Tooling
- Go 1.22+ (set `GOTOOLCHAIN=auto` unless project pins a version).
- Module management: `go mod tidy` to sync deps; vendoring only when required.
- Linting: `golangci-lint run` (or `staticcheck` if configured).
- Formatting: `gofmt -w` (or `go fmt ./...`).
- Testing: `go test ./...` with `-race` when feasible.
- Coverage: `go test -cover ./...`; for reports `go test -coverprofile=coverage.out ./...` and `go tool cover -html=coverage.out`.

## Project Layout
- `cmd/<app>/` for binaries; `internal/` for private packages; `pkg/` for shared packages (if allowed).
- `configs/` for config files; `scripts/` for tooling helpers; `deploy/` for manifests (if used).
- Keep generated artifacts (e.g., binaries) out of VCS; use `bin/` or `dist/` and gitignore them.

## Development Commands
- `go mod tidy` — sync module deps.
- `go test ./...` — unit tests; add `-race` where practical.
- `golangci-lint run` — lint (configure via `.golangci.yml`).
- `go fmt ./...` — format; `gofmt -w` for explicit writes.
- `go run ./cmd/<app>` — run main binary during development.

## Style & Naming
- Follow Go conventions: `MixedCaps` for exported names, `lowerCamelCase` for locals; package names short/lowercase.
- Keep interfaces small; prefer composition over inheritance.
- Use structured logging packages (`log/slog`, `zap`, or project standard) over bare `log.Printf` for production.

## Testing Guidance
- Co-locate tests with code as `_test.go`; use table-driven tests.
- Avoid network/filesystem access in unit tests unless marked/integration; gate with build tags if needed.
- Benchmarks live alongside tests with `_test.go` and `Benchmark*` names.

## Configuration & Ops
- Use env vars or config files; avoid embedding secrets. Consider `github.com/kelseyhightower/envconfig` or similar when appropriate.
- Pin tool versions in CI (Go toolchain, golangci-lint) for reproducibility.
- Run `go vet ./...` and security scanners (e.g., `gosec`) where applicable; document waivers.
