#!/usr/bin/env bash
set -euo pipefail

mapfile -t files < <(git diff --cached --name-only --diff-filter=ACM | rg '\\.md$' || true)
if [[ ${#files[@]} -eq 0 ]]; then
  exit 0
fi

python scripts/check-docs-quality.py "${files[@]}"
