# Stack Profile: AWS Lambda (Node/Python)

Use this profile for AWS Lambda functions (Node.js or Python). Pair it with the core governance rules in `AGENTS.md`.

## Runtime & Tooling
- Match runtime to function config (Node 18+/20, Python 3.11+).
- Package manager: npm/pip per language; deploy via SAM/Serverless/Terraform/CDK depending on repo.
- Lint/format/test per language stack profile (Node or Python).

## Project Layout
- Handler code under `src/` or per-function folders; infra under `template.yaml`, `serverless.yml`, or IaC folder.
- Keep build artifacts (`.aws-sam/`, `.serverless/`, `dist/`) out of VCS.

## Development Commands
- Node: `npm install`; `npm test`; `npm run lint`; `npm run build` if bundling.
- Python: `pip install -r requirements.txt`; `pytest`; `ruff`/`black`.
- Local invoke per framework: `sam local invoke`, `sls invoke local`, or CDK synth/deploy commands as defined.

## Style & Naming
- Follow language stack profile; keep handlers minimal and delegate to services.
- Structure env/config via parameters and env vars; avoid hardcoded ARNs.

## Testing Guidance
- Unit test handler logic with mocked AWS SDK; avoid live AWS in unit tests.
- Integration tests may use localstack or sandbox accounts; gate accordingly.

## Configuration & Ops
- Manage secrets via Lambda env vars + KMS/SM/SSM; never commit creds.
- Document deployment commands and stages; align runtime/tool versions with infra templates.
