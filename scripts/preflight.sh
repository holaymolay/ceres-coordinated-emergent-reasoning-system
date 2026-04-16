#!/usr/bin/env bash
set -euo pipefail

# Thin wrapper — delegates to preflight.py (the single implementation).
# Kept as preflight.sh so existing callers (.ceres/bin/preflight,
# autobootstrap.sh, docs, tests) continue to work without changes.

ROOT="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
if [[ "$ROOT" == *"/.ceres/"* || "$ROOT" == */.ceres ]]; then
  prefix="${ROOT%%/.ceres*}"
  [[ -n "$prefix" ]] && ROOT="$prefix"
fi
if [[ -n "${CERES_HOME:-}" && "$CERES_HOME" == */.ceres ]]; then
  ROOT="$(CDPATH= cd -- "${CERES_HOME%/.ceres}" && pwd)"
fi

exec python3 "$ROOT/scripts/preflight.py" "$@"
