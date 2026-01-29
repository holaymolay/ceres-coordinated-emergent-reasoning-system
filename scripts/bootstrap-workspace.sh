#!/usr/bin/env bash
set -euo pipefail

# Bootstrap nested CERES layout under .ceres/ with workspace + core submodule/clone.
# Idempotent: safe to re-run; skips existing files unless --force is provided for core ref rewrite.

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
SCRIPT_ROOT="$(CDPATH= cd -- "$SCRIPT_DIR/.." && pwd)"
ROOT_OVERRIDE=""
ROOT=""
DEFAULT_CORE_URL="${CORE_URL:-https://github.com/holaymolay/ceres-coordinated-emergent-reasoning-system.git}"
DEFAULT_CORE_REF="${CORE_REF:-}"
DEFAULT_WORKSPACE=".ceres/workspace"
COMPONENTS=false
CORE_URL="$DEFAULT_CORE_URL"
CORE_REF="$DEFAULT_CORE_REF"
WORKSPACE_REL="$DEFAULT_WORKSPACE"
FORCE_CORE_REF=false
NO_COMPONENTS=false
GIT_WAS_INIT=false

usage() {
  cat <<'USAGE'
Usage: scripts/bootstrap-workspace.sh [options]

Options:
  --core-url <url>        Core repo URL (default: https://github.com/holaymolay/ceres-coordinated-emergent-reasoning-system.git)
  --core-ref <ref>        Core tag/branch/commit to pin (default: remote HEAD)
  --workspace <path>      Workspace path (default: .ceres/workspace)
  --components            Clone component repos from repos.yaml into .ceres/components
  --no-components         Skip cloning components (faster init)
  --root <path>           Target repo root (default: git root or current directory)
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
    --no-components) NO_COMPONENTS=true; shift;;
    --root) ROOT_OVERRIDE="$2"; shift 2;;
    --force-core-ref) FORCE_CORE_REF=true; shift;;
    -h|--help) usage; exit 0;;
    *) echo "Unknown option: $1" >&2; usage; exit 1;;
  esac
done
if [[ "$NO_COMPONENTS" == "true" ]]; then
  COMPONENTS=false
fi

fail() { echo "ERROR: $*" >&2; exit 1; }
info() { echo "INFO: $*" >&2; }
warn() { echo "WARN: $*" >&2; }

require_git() {
  command -v git >/dev/null 2>&1 || fail "git is required"
}

detect_root() {
  if [[ -n "$ROOT_OVERRIDE" ]]; then
    ROOT="$ROOT_OVERRIDE"
    return
  fi
  local candidate
  candidate="$(git -C "$PWD" rev-parse --show-toplevel 2>/dev/null || true)"
  if [[ -n "$candidate" ]]; then
    ROOT="$candidate"
    return
  fi
  candidate="$(git -C "$SCRIPT_ROOT" rev-parse --show-toplevel 2>/dev/null || true)"
  if [[ -n "$candidate" ]]; then
    ROOT="$candidate"
    return
  fi
  ROOT="$PWD"
}

normalize_root() {
  if [[ "$ROOT" == *"/.ceres/"* || "$ROOT" == */.ceres ]]; then
    local prefix
    prefix="${ROOT%%/.ceres*}"
    if [[ -n "$prefix" ]]; then
      warn "Detected ROOT inside .ceres; normalizing to $prefix"
      ROOT="$prefix"
    fi
  fi
}

ensure_git_worktree() {
  if git -C "$ROOT" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    return
  fi
  info "Initializing git worktree in $ROOT"
  git -C "$ROOT" init >/dev/null
  git -C "$ROOT" add -A >/dev/null 2>&1 || true
  git -C "$ROOT" commit -m "Init workspace for CERES bootstrap" >/dev/null 2>&1 || true
  GIT_WAS_INIT=true
}

abs_path() {
  local path="$1"
  if [[ "$path" = /* ]]; then
    echo "$path"
  else
    echo "$ROOT/$path"
  fi
}

detect_core_ref() {
  if [[ -n "$CORE_REF" ]]; then
    return
  fi
  local ref
  ref="$(git ls-remote --symref "$CORE_URL" HEAD 2>/dev/null | awk '/^ref:/ {print $2}' | sed 's@refs/heads/@@')"
  if [[ -z "$ref" ]]; then
    ref="master"
  fi
  CORE_REF="$ref"
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
  local max_jobs="${COMPONENTS_PARALLEL:-4}"
  local jobs=0
  awk '
    /^- name:/ { name=$3 }
    /local_path:/ { local_path=$2; print name "|" local_path }
  ' "$repos_file" | while IFS='|' read -r NAME LOCAL_PATH; do
    [[ -z "$NAME" || -z "$LOCAL_PATH" ]] && continue
    local target="$dest_root/$LOCAL_PATH"
    if [[ -d "$target/.git" ]]; then
      info "Component present: $target"
      continue
    fi
    local remote="https://github.com/${org}/${NAME}.git"
    info "Cloning $NAME -> $target from $remote"
    git clone "$remote" "$target" &
    jobs=$((jobs + 1))
    if [[ "$jobs" -ge "$max_jobs" ]]; then
      wait -n 2>/dev/null || wait
      jobs=$((jobs - 1))
    fi
  done
  wait 2>/dev/null || true
}

init_workspace() {
  local workspace="$1"
  local template_root="$ROOT/templates"
  local elicitation_template="$ROOT/templates/elicitation/elicitation.md"
  if [[ ! -d "$template_root" && -d "$CORE_DIR/templates" ]]; then
    template_root="$CORE_DIR/templates"
    elicitation_template="$CORE_DIR/templates/elicitation/elicitation.md"
  fi
  local manifest=""
  if [[ -f "$ROOT/scripts/bootstrap-manifest.json" ]]; then
    manifest="$ROOT/scripts/bootstrap-manifest.json"
  elif [[ -f "$CORE_DIR/scripts/bootstrap-manifest.json" ]]; then
    manifest="$CORE_DIR/scripts/bootstrap-manifest.json"
  fi
  mkdir -p "$workspace"
  if [[ -n "$manifest" && -n "$(command -v python3)" ]]; then
    python3 - <<'PY' "$manifest" "$template_root" "$workspace"
import json
import os
import shutil
import sys
from pathlib import Path

manifest = Path(sys.argv[1])
base = Path(sys.argv[2])
workspace = Path(sys.argv[3])

data = json.loads(manifest.read_text(encoding="utf-8"))
for item in data.get("workspace", []):
    src = base / item["src"]
    dest = workspace / item["dest"]
    if dest.exists():
        continue
    dest.parent.mkdir(parents=True, exist_ok=True)
    if src.exists():
        shutil.copyfile(src, dest)
for rel in data.get("workspace_dirs", []):
    (workspace / rel).mkdir(parents=True, exist_ok=True)
PY
  else
    copy_if_missing "$template_root/todo/todo-inbox.md" "$workspace/todo-inbox.md"
    copy_if_missing "$template_root/todo/todo.md" "$workspace/todo.md"
    copy_if_missing "$template_root/todo/completed.md" "$workspace/completed.md"
    copy_if_missing "$template_root/todo/memory.md" "$workspace/memory.md"
    copy_if_missing "$template_root/todo/handover.md" "$workspace/handover.md"
    copy_if_missing "$template_root/artifacts/objective-contract.json" "$workspace/objective-contract.json"
    copy_if_missing "$template_root/artifacts/gap-ledger.json" "$workspace/gap-ledger.json"
    copy_if_missing "$elicitation_template" "$workspace/specs/elicitation/elicitation.md"
    mkdir -p "$workspace/prompts" "$workspace/memory/records" "$workspace/logs" "$workspace/synchronizations" "$workspace/concepts"
  fi
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
  if [[ -d "$bin_src" && -d "$bin_dest" && "$bin_src" -ef "$bin_dest" ]]; then
    info "Wrapper source and destination are the same; skipping copy."
    return
  fi
  for f in "$bin_src"/*; do
    [[ -f "$f" ]] || continue
    cp "$f" "$bin_dest/$(basename "$f")"
    chmod +x "$bin_dest/$(basename "$f")"
  done
  info "Installed wrappers to $bin_dest"
}

require_git
detect_root
normalize_root
ROOT="$(CDPATH= cd -- "$ROOT" && pwd)"
detect_core_ref
ensure_git_worktree

CERES_HOME_DIR="$ROOT/.ceres"
WORKSPACE_DIR="$(abs_path "$WORKSPACE_REL")"
CORE_DIR="$CERES_HOME_DIR/core"
CORE_LOCK="$CERES_HOME_DIR/core.lock"
COMPONENTS_DIR="$CERES_HOME_DIR/components"
CORE_SUBMODULE_PATH=".ceres/core"

mkdir -p "$CERES_HOME_DIR"

if [[ -d "$CORE_DIR" ]]; then
  if [[ -d "$CORE_DIR/.git" ]]; then
    info "Core already present at $CORE_DIR"
  else
    info "Core directory present without git metadata; using as-is"
  fi
  if [[ "$FORCE_CORE_REF" == "true" ]]; then
    info "Updating core to ref $CORE_REF"
    git -C "$CORE_DIR" fetch --all
    git -C "$CORE_DIR" checkout "$CORE_REF"
  fi
else
  if [[ "$GIT_WAS_INIT" == "true" ]]; then
    info "Cloning core into $CORE_DIR @ $CORE_REF (non-submodule)"
    if ! git clone --depth 1 --branch "$CORE_REF" "$CORE_URL" "$CORE_DIR"; then
      warn "Clone with ref $CORE_REF failed; retrying default HEAD"
      git clone --depth 1 "$CORE_URL" "$CORE_DIR"
    fi
  else
    info "Adding core submodule from $CORE_URL @ $CORE_REF"
    git -C "$ROOT" submodule add "$CORE_URL" "$CORE_SUBMODULE_PATH"
    (cd "$CORE_DIR" && git checkout "$CORE_REF") || warn "Core checkout failed; continuing"
  fi
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
