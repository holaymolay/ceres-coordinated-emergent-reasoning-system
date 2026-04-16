#!/usr/bin/env bash
set -euo pipefail

repo_root="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
venv_dir="${SKILLCTL_VENV:-$repo_root/.venv-skillctl}"

python3 -m venv "$venv_dir"
"$venv_dir/bin/pip" install -q -r "$repo_root/scripts/requirements-skillctl.txt"

printf 'skillctl venv ready: %s\n' "$venv_dir"

