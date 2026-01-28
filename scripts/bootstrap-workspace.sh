#!/usr/bin/env bash
set -euo pipefail

# Bootstrap nested CERES layout under .ceres/ with workspace + core submodule.
# Idempotent: safe to re-run; skips existing files unless --force is provided for core ref rewrite.

ROOT="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
DEFAULT_CORE_URL="${CORE_URL:-https://github.com/holaymolay/ceres-coordinated-emergent-reasoning-system.git}"
DEFAULT_CORE_REF="${CORE_REF:-main}"
DEFAULT_WORKSPACE=".ceres/workspace"
COMPONENTS=false
CORE_URL="$DEFAULT_CORE_URL"
CORE_REF="$DEFAULT_CORE_REF"
WORKSPACE_REL="$DEFAULT_WORKSPACE"
FORCE_CORE_REF=false

usage() {
  cat <<'USAGE'
Usage: scripts/bootstrap-workspace.sh [options]

Options:
  --core-url <url>        Core repo URL (default: https://github.com/holaymolay/ceres-coordinated-emergent-reasoning-system.git)
  --core-ref <ref>        Core tag/branch/commit to pin (default: main)
  --workspace <path>      Workspace path (default: .ceres/workspace)
  --components            Clone component repos from repos.yaml into .ceres/components
  --force-core-ref        If core exists, reset checkout to the requested ref (otherwise leave as-is)
  -h|--help               Show this help
USAGE
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --core-url) CORE_URL="$2"; shift 2;;
    --core-ref) CORE_REF="$2"; shift 2;;
    --workspace) WORKSPACE_REL="$2"; shift 2;;
    --components) COMPONENTS=true; shift;;
    --force-core-ref) FORCE_CORE_REF=true; shift;;
    -h|--help) usage; exit 0;;
    *) echo "Unknown option: $1" >&2; usage; exit 1;;
  esac
done

fail() { echo "ERROR: $*" >&2; exit 1; }
info() { echo "INFO: $*" >&2; }

require_git() {
  command -v git >/dev/null 2>&1 || fail "git is required"
}

ensure_git_worktree() {
  if git -C "$ROOT" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    return
  fi
  info "Initializing git worktree in $ROOT"
  git -C "$ROOT" init >/dev/null
  git -C "$ROOT" add -A >/dev/null 2>&1 || true
  git -C "$ROOT" commit -m "Init workspace for CERES bootstrap" >/dev/null 2>&1 || true
}

abs_path() {
  local path="$1"
  if [[ "$path" = /* ]]; then
    echo "$path"
  else
    echo "$ROOT/$path"
  fi
}

write_core_lock() {
  local core_dir="$1"
  local lock_path="$2"
  local core_remote="$3"
  local core_ref="$4"
  local commit="unknown"
  if [[ -d "$core_dir/.git" ]]; then
    commit="$(git -C "$core_dir" rev-parse HEAD 2>/dev/null || echo "unknown")"
  fi
  cat > "$lock_path" <<EOF
remote: $core_remote
ref: $core_ref
commit: $commit
generated_at: $(date -u +"%Y-%m-%dT%H:%M:%SZ")
EOF
  info "Wrote core.lock -> $lock_path"
}

copy_if_missing() {
  local src="$1"
  local dest="$2"
  if [[ -e "$dest" ]]; then
    info "Skip existing $dest"
  else
    mkdir -p "$(dirname "$dest")"
    cp "$src" "$dest"
    info "Created $dest"
  fi
}

clone_components() {
  local dest_root="$1"
  local repos_file="$ROOT/repos.yaml"
  if [[ ! -f "$repos_file" && -f "$CORE_DIR/repos.yaml" ]]; then
    repos_file="$CORE_DIR/repos.yaml"
  fi
  local org="${COMPONENT_ORG:-holaymolay}"
  [[ -f "$repos_file" ]] || { info "repos.yaml not found; skipping components"; return; }
  mkdir -p "$dest_root"
  awk '
    /^- name:/ { name=$3 }
    /local_path:/ { path=$2; print name "|" path }
  ' "$repos_file" | while IFS='|' read -r NAME PATH; do
    [[ -z "$NAME" || -z "$PATH" ]] && continue
    local target="$dest_root/$PATH"
    if [[ -d "$target/.git" ]]; then
      info "Component present: $target"
      continue
    fi
    local remote="https://github.com/${org}/${NAME}.git"
    info "Cloning $NAME -> $target from $remote"
    git clone "$remote" "$target"
  done
}

init_workspace() {
  local workspace="$1"
  mkdir -p "$workspace"
  copy_if_missing "$ROOT/templates/todo/todo-inbox.md" "$workspace/todo-inbox.md"
  copy_if_missing "$ROOT/templates/todo/todo.md" "$workspace/todo.md"
  copy_if_missing "$ROOT/templates/todo/completed.md" "$workspace/completed.md"
  copy_if_missing "$ROOT/templates/todo/memory.md" "$workspace/memory.md"
  copy_if_missing "$ROOT/templates/todo/handover.md" "$workspace/handover.md"
  copy_if_missing "$ROOT/templates/artifacts/objective-contract.json" "$workspace/objective-contract.json"
  copy_if_missing "$ROOT/templates/artifacts/gap-ledger.json" "$workspace/gap-ledger.json"
  copy_if_missing "$ROOT/templates/elicitation/elicitation.md" "$workspace/specs/elicitation/elicitation.md"
  mkdir -p "$workspace/prompts" "$workspace/memory/records" "$workspace/logs" "$workspace/synchronizations" "$workspace/concepts"
}

install_wrappers() {
  local home="$1"
  local bin_src="$ROOT/.ceres/bin"
  if [[ ! -d "$bin_src" && -d "$CORE_DIR/.ceres/bin" ]]; then
    bin_src="$CORE_DIR/.ceres/bin"
  fi
  local bin_dest="$home/bin"
  if [[ ! -d "$bin_src" ]]; then
    info "Wrapper source $bin_src missing; skipping wrapper install"
    return
  fi
  mkdir -p "$bin_dest"
  for f in "$bin_src"/*; do
    [[ -f "$f" ]] || continue
    cp "$f" "$bin_dest/$(basename "$f")"
    chmod +x "$bin_dest/$(basename "$f")"
  done
  info "Installed wrappers to $bin_dest"
}

require_git
ensure_git_worktree

CERES_HOME_DIR="$ROOT/.ceres"
WORKSPACE_DIR="$(abs_path "$WORKSPACE_REL")"
CORE_DIR="$CERES_HOME_DIR/core"
CORE_LOCK="$CERES_HOME_DIR/core.lock"
COMPONENTS_DIR="$CERES_HOME_DIR/components"

mkdir -p "$CERES_HOME_DIR"

if [[ -d "$CORE_DIR/.git" ]]; then
  info "Core already present at $CORE_DIR"
  if [[ "$FORCE_CORE_REF" == "true" ]]; then
    info "Updating core to ref $CORE_REF"
    git -C "$CORE_DIR" fetch --all
    git -C "$CORE_DIR" checkout "$CORE_REF"
  fi
else
  info "Adding core submodule from $CORE_URL @ $CORE_REF"
  git submodule add "$CORE_URL" "$CORE_DIR"
  (cd "$CORE_DIR" && git checkout "$CORE_REF")
fi

write_core_lock "$CORE_DIR" "$CORE_LOCK" "$CORE_URL" "$CORE_REF"
init_workspace "$WORKSPACE_DIR"
install_wrappers "$CERES_HOME_DIR"

if [[ "$COMPONENTS" == "true" ]]; then
  clone_components "$COMPONENTS_DIR"
fi

info "Bootstrap complete."
echo "CERES_HOME=$CERES_HOME_DIR"
echo "CERES_WORKSPACE=$WORKSPACE_DIR"
