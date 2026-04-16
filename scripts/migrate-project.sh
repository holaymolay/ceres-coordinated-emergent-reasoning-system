#!/usr/bin/env bash
set -euo pipefail

# Migrate a consumer project from old multi-repo CERES to the new monorepo version.
#
# Usage:
#   /path/to/ceres/scripts/migrate-project.sh /path/to/consumer-project
#
# What this does:
#   1. Backs up .ceres/workspace/ (your project's actual work state — preserved)
#   2. Removes old .ceres/core/ (submodule or tarball extraction)
#   3. Removes .ceres/components/ (components are now part of core)
#   4. Removes stale .gitmodules entries for .ceres/core
#   5. Re-installs .ceres/core/ from the new monorepo (clone --depth 1)
#   6. Re-runs bootstrap to update wrappers in .ceres/bin/
#   7. Adds harness pointer files (CLAUDE.md, GEMINI.md, .cursorrules) if missing
#   8. Runs harness detection and state digest generation
#   9. Reports what changed
#
# Safe to re-run (idempotent). Workspace artifacts are never overwritten.

CERES_REPO_URL="https://github.com/holaymolay/ceres-coordinated-emergent-reasoning-system.git"
SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"

log()  { echo "  [migrate] $*"; }
warn() { echo "  [migrate] WARN: $*" >&2; }

usage() {
  echo "Usage: $0 <project-root>"
  echo ""
  echo "Migrates a consumer project from old multi-repo CERES to the new monorepo."
  echo "Preserves .ceres/workspace/ (your project's work state)."
  exit 1
}

[[ $# -ge 1 ]] || usage
PROJECT="$(CDPATH= cd -- "$1" && pwd)"
[[ -d "$PROJECT" ]] || { echo "ERROR: $PROJECT is not a directory" >&2; exit 1; }

CERES_HOME="$PROJECT/.ceres"
WORKSPACE="$CERES_HOME/workspace"
CORE="$CERES_HOME/core"
COMPONENTS="$CERES_HOME/components"
BACKUP="/tmp/ceres-migrate-backup-$(date +%s)"

echo "=== CERES Migration ==="
echo "Project: $PROJECT"
echo "Backup:  $BACKUP"
echo ""

# ── Step 1: Backup workspace ──
if [[ -d "$WORKSPACE" ]]; then
  log "Backing up workspace..."
  mkdir -p "$BACKUP"
  cp -a "$WORKSPACE" "$BACKUP/workspace"
  log "Workspace backed up to $BACKUP/workspace"
else
  log "No existing workspace found (fresh project)."
fi

# ── Step 2: Remove old .ceres/core/ ──
if [[ -d "$CORE" ]]; then
  # Handle submodule case
  if [[ -f "$PROJECT/.gitmodules" ]] && grep -q ".ceres/core" "$PROJECT/.gitmodules" 2>/dev/null; then
    log "Removing .ceres/core submodule..."
    (
      cd "$PROJECT"
      git submodule deinit .ceres/core 2>/dev/null || true
      git rm --cached .ceres/core 2>/dev/null || true
      git config --remove-section "submodule..ceres/core" 2>/dev/null || true
      rm -rf ".git/modules/.ceres/core" 2>/dev/null || true
    )
    # Clean .gitmodules — remove the .ceres/core entry
    if [[ -f "$PROJECT/.gitmodules" ]]; then
      python3 -c "
import re, sys
path = sys.argv[1]
text = open(path).read()
text = re.sub(r'\[submodule \".ceres/core\"\][^\[]*', '', text, flags=re.DOTALL).strip()
if text:
    open(path, 'w').write(text + '\n')
else:
    import os; os.remove(path)
" "$PROJECT/.gitmodules" 2>/dev/null || true
    fi
  fi
  rm -rf "$CORE"
  log "Removed old .ceres/core/"
else
  log "No existing .ceres/core/ found."
fi

# ── Step 3: Remove old .ceres/components/ ──
if [[ -d "$COMPONENTS" ]]; then
  log "Removing .ceres/components/ (components are now part of core)..."
  rm -rf "$COMPONENTS"
  log "Removed .ceres/components/"
else
  log "No .ceres/components/ found (already clean)."
fi

# ── Step 4: Remove stale core.lock ──
rm -f "$CERES_HOME/core.lock"

# ── Step 5: Install new .ceres/core/ from monorepo ──
log "Installing new .ceres/core/ from monorepo..."
mkdir -p "$CERES_HOME"
if command -v git >/dev/null 2>&1; then
  git clone --depth 1 "$CERES_REPO_URL" "$CORE" 2>&1 | tail -2
else
  warn "git not available; attempting tarball fallback..."
  mkdir -p "$CORE"
  curl -fsSL "https://github.com/holaymolay/ceres-coordinated-emergent-reasoning-system/releases/latest/download/ceres-fast.tar.gz" -o /tmp/ceres-fast.tgz
  tar -xzf /tmp/ceres-fast.tgz -C "$CORE" --strip-components 1
fi
log "Installed new .ceres/core/"

# ── Step 6: Re-run bootstrap to update wrappers ──
log "Re-running bootstrap..."
if [[ -x "$CORE/scripts/bootstrap-workspace.sh" ]]; then
  bash "$CORE/scripts/bootstrap-workspace.sh" --root "$PROJECT" 2>&1 | grep -E "^(INFO|WARN)" || true
fi
log "Bootstrap complete."

# ── Step 7: Restore workspace (bootstrap won't overwrite existing files) ──
if [[ -d "$BACKUP/workspace" ]]; then
  # Copy back anything that bootstrap might not have preserved
  cp -an "$BACKUP/workspace/"* "$WORKSPACE/" 2>/dev/null || true
  log "Workspace state preserved."
fi

# ── Step 8: Add harness pointer files if missing ──
SHIM_CONTENT="This project uses CERES. Read AGENTS.md for governance rules and PROMPTLOADER.md for bootstrap."
for shim in CLAUDE.md GEMINI.md .cursorrules; do
  if [[ ! -f "$PROJECT/$shim" ]]; then
    echo "$SHIM_CONTENT" > "$PROJECT/$shim"
    log "Created $shim"
  fi
done

# ── Step 9: Run harness detection and state digest ──
if command -v python3 >/dev/null 2>&1; then
  if [[ -f "$CORE/scripts/detect-harness.py" ]]; then
    CERES_WORKSPACE="$WORKSPACE" python3 "$CORE/scripts/detect-harness.py" 2>/dev/null || true
  fi
  if [[ -f "$CORE/scripts/generate-state-digest.py" ]]; then
    CERES_WORKSPACE="$WORKSPACE" python3 "$CORE/scripts/generate-state-digest.py" 2>/dev/null || true
  fi
fi

# ── Step 10: Add .ceres/core/ to .gitignore if not already ──
if [[ -f "$PROJECT/.gitignore" ]]; then
  if ! grep -q "^\.ceres/core/" "$PROJECT/.gitignore" 2>/dev/null; then
    echo "" >> "$PROJECT/.gitignore"
    echo "# CERES core (installed, not tracked)" >> "$PROJECT/.gitignore"
    echo ".ceres/core/" >> "$PROJECT/.gitignore"
    echo ".ceres/core.lock" >> "$PROJECT/.gitignore"
    log "Added .ceres/core/ to .gitignore"
  fi
elif [[ -d "$PROJECT/.git" ]]; then
  cat > "$PROJECT/.gitignore" <<'GITIGNORE'
# CERES core (installed, not tracked)
.ceres/core/
.ceres/core.lock
GITIGNORE
  log "Created .gitignore with .ceres/core/ entry"
fi

echo ""
echo "=== Migration complete ==="
echo "Project:   $PROJECT"
echo "Core:      $CORE (new monorepo)"
echo "Workspace: $WORKSPACE (preserved)"
echo "Backup:    $BACKUP"
echo ""
echo "Next steps:"
echo "  1. Verify: cd $PROJECT && ./.ceres/bin/autobootstrap"
echo "  2. If everything works, you can delete $BACKUP"
echo "  3. Commit the changes if you want them tracked"
