#!/usr/bin/env bash
set -euo pipefail

# Resolve CERES paths with priority:
# 1) CERES_HOME env or default .ceres relative to repo root
# 2) CERES_WORKSPACE env or CERES_HOME/workspace if present, else repo root

BIN_DIR="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(CDPATH= cd -- "$BIN_DIR/../.." && pwd)"

CERES_HOME="${CERES_HOME:-$REPO_ROOT/.ceres}"
if [[ -n "${CERES_WORKSPACE:-}" ]]; then
  CERES_WORKSPACE="${CERES_WORKSPACE}"
elif [[ -d "$CERES_HOME/workspace" ]]; then
  CERES_WORKSPACE="$CERES_HOME/workspace"
else
  CERES_WORKSPACE="$REPO_ROOT"
fi

CORE_DIR="$CERES_HOME/core"
CORE_LOCK="$CERES_HOME/core.lock"

export CERES_HOME CERES_WORKSPACE

resolve_script() {
  local candidate="$1"
  if [[ -x "$CORE_DIR/scripts/$candidate" ]]; then
    check_core_lock
    echo "$CORE_DIR/scripts/$candidate"
    return 0
  fi
  if [[ -f "$CORE_DIR/scripts/${candidate%.py}.py" ]]; then
    check_core_lock
    echo "$CORE_DIR/scripts/${candidate%.py}.py"
    return 0
  fi
  if [[ -x "$REPO_ROOT/scripts/$candidate" ]]; then
    echo "$REPO_ROOT/scripts/$candidate"
    return 0
  fi
  if [[ -f "$REPO_ROOT/scripts/${candidate%.py}.py" ]]; then
    echo "$REPO_ROOT/scripts/${candidate%.py}.py"
    return 0
  fi
  return 1
}

check_core_lock() {
  [[ -d "$CORE_DIR/.git" ]] || return 0
  [[ -f "$CORE_LOCK" ]] || return 0
  local lock_commit
  lock_commit="$(awk -F': ' '/^commit:/ {print $2}' "$CORE_LOCK" | head -n1)"
  if [[ -z "$lock_commit" ]]; then
    return 0
  fi
  local current_commit
  current_commit="$(git -C "$CORE_DIR" rev-parse HEAD 2>/dev/null || true)"
  if [[ -n "$current_commit" && "$lock_commit" != "$current_commit" ]]; then
    echo "ERROR: core.lock commit ($lock_commit) does not match core submodule ($current_commit)" >&2
    exit 1
  fi
}
