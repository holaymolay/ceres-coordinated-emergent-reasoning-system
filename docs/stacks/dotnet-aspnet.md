# Stack Profile: .NET / ASP.NET Core

Use this profile for .NET services built with ASP.NET Core. Pair it with the core governance rules in `AGENTS.md`.

## Runtime & Tooling
- .NET SDK 8.0 (match repo `global.json` if present).
- Dependency/build tool: `dotnet` CLI.
- Lint/format: `dotnet format`; analyzers via `dotnet build`/`dotnet test` with warnings as errors when enforced.
- Testing: `dotnet test`; coverage via `coverlet` or `dotnet test /p:CollectCoverage=true` (project-dependent).

## Project Layout
- Solution files (`*.sln`) at root; projects under feature folders (e.g., `src/`, `tests/`).
- API projects typically under `src/<Project>.Api`; shared libs under `src/<Project>.Domain`/`Application`/`Infrastructure`.
- Keep build artifacts under `bin/` and `obj/` (ignored).

## Development Commands
- `dotnet restore` — restore packages.
- `dotnet build` — compile; add `-warnaserror` if required.
- `dotnet test` — run tests; add coverage flags per project conventions.
- `dotnet run --project src/<Project>.Api` — run service locally.
- `dotnet format` — format and apply analyzers (if configured).

## Style & Naming
- Follow project analyzers/style rules; prefer `ILogger<>` for logging.
- Use PascalCase for types/methods, camelCase for locals/params; namespaces align to folder structure.
- Avoid `Console.WriteLine` in committed code; rely on logging abstractions.

## Testing Guidance
- Tests under `tests/` mirroring project structure; use xUnit/NUnit/MSTest per repo standard.
- Keep unit tests isolated; mock external dependencies; use integration tests with test server/containers when needed.
- Measure coverage if enforced; keep deterministic data builders/fixtures.

## Configuration & Ops
- Configuration via `appsettings.json` + environment-specific overrides; do not commit secrets.
- Use `dotnet user-secrets` for local secrets when applicable.
- Run `dotnet list package --vulnerable` or org-standard security scans; document waivers.
