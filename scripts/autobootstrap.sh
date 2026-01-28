#!/usr/bin/env bash
set -euo pipefail

# Non-interactive CERES autobootstrap. Always proceeds; logs warnings only.

ROOT="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
CERES_HOME="$ROOT/.ceres"
WORKSPACE="$CERES_HOME/workspace"
QUARANTINE_ROOT="$CERES_HOME/_quarantine"
TS="$(date -u +"%Y%m%dT%H%M%SZ")"

log() { echo "INFO: $*" >&2; }
warn() { echo "WARN: $*" >&2; }

quarantine_path() {
  local label="$1"
  local target="$QUARANTINE_ROOT/$TS/$label"
  mkdir -p "$target"
  echo "$target"
}

quarantine_if_exists() {
  local path="$1"
  local label="$2"
  if [[ -e "$path" ]]; then
    local dest
    dest="$(quarantine_path "$label")"
    mv "$path" "$dest/" 2>/dev/null || true
    warn "Quarantined $path -> $dest"
  fi
}

quarantine_stray_artifacts() {
  if [[ -d "$WORKSPACE" ]]; then
    quarantine_if_exists "$ROOT/todo-inbox.md" "root-artifacts"
    quarantine_if_exists "$ROOT/todo.md" "root-artifacts"
    quarantine_if_exists "$ROOT/completed.md" "root-artifacts"
    quarantine_if_exists "$ROOT/memory.md" "root-artifacts"
    quarantine_if_exists "$ROOT/handover.md" "root-artifacts"
    quarantine_if_exists "$ROOT/objective-contract.json" "root-artifacts"
    quarantine_if_exists "$ROOT/gap-ledger.json" "root-artifacts"
    quarantine_if_exists "$ROOT/specs" "root-artifacts"
  fi
}

bootstrap() {
  if [[ ! -x "$ROOT/scripts/bootstrap-workspace.sh" ]]; then
    warn "bootstrap-workspace.sh missing; cannot bootstrap core"
    return
  fi
  bash "$ROOT/scripts/bootstrap-workspace.sh" --components || warn "bootstrap-workspace.sh reported errors"
}

ensure_workspace_artifacts() {
  if [[ -x "$ROOT/scripts/init-artifacts.sh" ]]; then
    bash "$ROOT/scripts/init-artifacts.sh" "$WORKSPACE" || warn "init-artifacts failed"
  fi
  mkdir -p "$WORKSPACE"
  mkdir -p "$WORKSPACE/memory/records" "$WORKSPACE/logs" "$WORKSPACE/prompts" "$WORKSPACE/concepts" "$WORKSPACE/synchronizations"
  [[ -f "$WORKSPACE/todo-inbox.md" ]] || cp "$ROOT/templates/todo/todo-inbox.md" "$WORKSPACE/todo-inbox.md" 2>/dev/null || true
  [[ -f "$WORKSPACE/todo.md" ]] || cp "$ROOT/templates/todo/todo.md" "$WORKSPACE/todo.md" 2>/dev/null || true
  [[ -f "$WORKSPACE/completed.md" ]] || cp "$ROOT/templates/todo/completed.md" "$WORKSPACE/completed.md" 2>/dev/null || true
  [[ -f "$WORKSPACE/memory.md" ]] || cp "$ROOT/templates/todo/memory.md" "$WORKSPACE/memory.md" 2>/dev/null || true
  [[ -f "$WORKSPACE/handover.md" ]] || cp "$ROOT/templates/todo/handover.md" "$WORKSPACE/handover.md" 2>/dev/null || true
}

run_preflight() {
  if [[ -x "$CERES_HOME/bin/preflight" ]]; then
    "$CERES_HOME/bin/preflight" --mode execute --prompt "$WORKSPACE/todo-inbox.md" --todo "$WORKSPACE/todo.md" \
      --gap-ledger "$WORKSPACE/gap-ledger.json" --objective "$WORKSPACE/objective-contract.json" >/dev/null 2>&1 || \
      warn "preflight reported issues (continuing)"
    return
  fi
  if [[ -x "$ROOT/scripts/preflight.sh" ]]; then
    "$ROOT/scripts/preflight.sh" --mode execute --prompt "$WORKSPACE/todo-inbox.md" --todo "$WORKSPACE/todo.md" \
      --gap-ledger "$WORKSPACE/gap-ledger.json" --objective "$WORKSPACE/objective-contract.json" >/dev/null 2>&1 || \
      warn "preflight reported issues (continuing)"
  fi
}

start_session() {
  if [[ -x "$CERES_HOME/bin/start-session" ]]; then
    "$CERES_HOME/bin/start-session" >/dev/null 2>&1 || warn "start-session failed"
    return
  fi
  if [[ -x "$ROOT/scripts/start-session.sh" ]]; then
    "$ROOT/scripts/start-session.sh" >/dev/null 2>&1 || warn "start-session failed"
  fi
}

main() {
  quarantine_stray_artifacts
  bootstrap
  ensure_workspace_artifacts
  run_preflight
  start_session
  log "CERES READY — next prompt should describe the project."
  exit 0
}

main
