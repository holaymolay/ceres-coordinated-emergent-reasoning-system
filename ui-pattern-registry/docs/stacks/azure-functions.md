# Stack Profile: Azure Functions

Use this profile for Azure Functions (Node/Python/.NET). Pair it with the core governance rules in `AGENTS.md`.

## Runtime & Tooling
- Match runtime to app settings (Node, Python, .NET); follow language stack profile for lint/test.
- Tooling: Azure Functions Core Tools, Azure CLI; IaC via Bicep/Terraform if present.

## Project Layout
- Functions in `functions/` or root with `function.json`; shared code in `shared/` or language-specific folders.
- Ignore build/artifact folders (e.g., `bin/`, `obj/`, `.python_packages/`, `dist/`).

## Development Commands
- Install deps per language manager.
- Run locally: `func start` (after `func extensions install` if needed).
- Tests: run per language stack; include integration tests with storage emulator when defined.

## Style & Naming
- Thin function handlers delegating to services; follow language lint/style rules.
- Keep configuration out of code; use app settings.

## Testing Guidance
- Unit test handlers with mocked Azure SDK; avoid live Azure in unit tests.
- Integration tests can target emulator or staging; gate accordingly.

## Configuration & Ops
- Manage settings via `local.settings.json` (local only) and app settings in Azure; never commit secrets.
- Document deployment commands (`func azure functionapp publish`, `az deployment`, IaC workflows) and required envs.
