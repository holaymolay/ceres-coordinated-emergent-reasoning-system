#!/usr/bin/env bash
set -euo pipefail

repo_root="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"

if [[ ! -x "$repo_root/.venv-skillctl/bin/python" ]]; then
  "$repo_root/scripts/setup-skillctl-venv.sh" >/dev/null
fi

"$repo_root/scripts/skillctl" validate --allow-template "$repo_root/skills/_template"

stdout_file="$(mktemp)"
trap 'rm -f "$stdout_file"' EXIT

"$repo_root/scripts/skillctl" run --allow-template "$repo_root/skills/_template" \
  --input "$repo_root/skills/_template/fixtures/input.json" \
  >"$stdout_file" 2>/dev/null

diff -u "$repo_root/skills/_template/fixtures/output.expected.json" "$stdout_file"
