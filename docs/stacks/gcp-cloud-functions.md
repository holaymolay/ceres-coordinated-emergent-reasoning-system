# Stack Profile: GCP Cloud Functions / Cloud Run

Use this profile for GCP serverless workloads (Functions/Cloud Run). Pair it with the core governance rules in `AGENTS.md`.

## Runtime & Tooling
- Match runtime to service (Node 20, Python 3.11, Go, etc.); follow language stack profile for lint/test.
- Deployment tooling: `gcloud`/`terraform`/`skaffold` per repo.

## Project Layout
- Function code under `functions/` or `src/`; Cloud Run services in app folders with `Dockerfile`.
- Ignore build artifacts (`.gcloud/`, `dist/`, container outputs).

## Development Commands
- Install deps via language manager (npm/pip/go/etc.).
- Local dev: `functions-framework`/`gcloud functions` emulator or `docker compose up`/`skaffold dev` for Cloud Run.
- Tests: run per language profile; include integration tests against emulators where defined.

## Style & Naming
- Keep handlers thin; push logic into services; follow language profile style/lint rules.
- Use structured logging per GCP recommendations.

## Testing Guidance
- Unit test handlers with mocked GCP clients; avoid live GCP in unit tests.
- Integration tests can target emulator/Cloud Run staging; gate appropriately.

## Configuration & Ops
- Manage config via env vars/Secrets Manager; avoid committing service accounts/keys.
- Document deploy commands (`gcloud functions deploy`, `gcloud run deploy`, terraform apply) and required envs.
