#!/usr/bin/env bash
set -euo pipefail

repo_root="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../.." && pwd)"

if ! "$repo_root/scripts/verify-sync.sh" >/dev/null 2>&1; then
  branch="$(git -C "$repo_root" rev-parse --abbrev-ref HEAD 2>/dev/null || echo "<unknown>")"
  echo
  echo "[post-commit] Branch ${branch} is not synchronized with its upstream."
  echo "[post-commit] Push now with: git push --set-upstream origin ${branch}"
  echo "[post-commit] (This hook is advisory and does not block commits.)"
fi

exit 0
