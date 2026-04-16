# Stack Profile: Ansible

Use this profile for configuration management with Ansible. Pair it with the core governance rules in `AGENTS.md`.

## Runtime & Tooling
- Ansible version per project; use virtualenv (`python -m venv .venv`) and `pip install -r requirements.txt`.
- Lint/format: `ansible-lint`; YAML formatting per project style.
- Testing: `molecule test` when configured.

## Project Layout
- Playbooks under `playbooks/` or root; roles under `roles/`; inventories under `inventories/` or `hosts` files; group_vars/host_vars for vars.
- Keep secrets in vault files; never commit plaintext secrets.

## Development Commands
- `python -m venv .venv && source .venv/bin/activate`
- `pip install -r requirements.txt` (include `ansible-lint`, `molecule` if used)
- `ansible-lint` on playbooks/roles
- `molecule test` for role scenarios when defined

## Style & Naming
- Use descriptive role/play names; avoid duplication; prefer variables over hardcoded values.
- Keep tasks idempotent.

## Testing Guidance
- Use Molecule with local/docker drivers; keep scenarios fast; avoid hitting real infra unless required.

## Configuration & Ops
- Encrypt secrets with Ansible Vault; manage vault passwords securely.
- Document inventory layout and execution commands (`ansible-playbook ...`) and required env vars.
