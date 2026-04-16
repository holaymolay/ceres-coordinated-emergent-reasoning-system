# Stack Profile: Terraform

Use this profile for IaC work with Terraform. Pair it with the core governance rules in `AGENTS.md`.

## Runtime & Tooling
- Terraform CLI version pinned via `.terraform-version`/`tfenv`/`asdf` or documented; prefer matching CI.
- Formatter/lint: `terraform fmt`; `tflint`/`tfsec`/`checkov` if configured.
- Testing: `terraform validate`; optional `terratest`/policy checks.

## Project Layout
- Modules under `modules/`; environments/stacks under `env/` or root workspaces; keep `.terraform/` ignored.
- Backend/state config via remote backends; never commit state files.

## Development Commands
- `terraform init` (with backend config)
- `terraform fmt -recursive`
- `terraform validate`
- `tflint` / `tfsec` / `checkov` as configured
- `terraform plan` (non-destructive) and `terraform apply` when approved

## Style & Naming
- Keep variables/outputs descriptive; use modules; avoid hardcoded creds.

## Testing Guidance
- Prefer `terraform plan` for review; use terratest/policy as code when available; avoid applying in non-approved contexts.

## Configuration & Ops
- Store state remotely (S3/GCS/AzureRM) with locking; manage secrets via vars/secret stores.
- Document workspace/env naming and required backend config.
