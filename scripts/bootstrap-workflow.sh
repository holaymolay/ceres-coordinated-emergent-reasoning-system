#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage: scripts/bootstrap-workflow.sh [--with-skills] [--force] [--dry-run] <target-dir>

Copies the workflow governance files into <target-dir> and creates empty
todo/ledger templates. Existing files are skipped unless --force is set.

Options:
  --with-skills  Include the Skill system scaffolding, docs, and tooling.
  --force        Overwrite existing files/directories when possible.
  --dry-run      Print intended actions without writing files.
  -h, --help     Show this help text.
EOF
}

repo_root="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
with_skills=0
force=0
dry_run=0
target=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --with-skills)
      with_skills=1
      shift
      ;;
    --force)
      force=1
      shift
      ;;
    --dry-run)
      dry_run=1
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      if [[ -z "$target" ]]; then
        target="$1"
        shift
      else
        printf 'Error: unexpected argument: %s\n' "$1" >&2
        usage
        exit 1
      fi
      ;;
  esac
done

if [[ -z "$target" ]]; then
  usage
  exit 1
fi

mkdir -p "$target"
target_root="$(CDPATH= cd -- "$target" && pwd)"

if [[ "$target_root" == "$repo_root" ]]; then
  printf 'Error: target directory cannot be the workflow repo root.\n' >&2
  exit 1
fi

log() {
  printf '%s\n' "$*"
}

copy_path() {
  local rel="$1"
  local src="$repo_root/$rel"
  local dst="$target_root/$rel"

  if [[ ! -e "$src" ]]; then
    log "Skip missing source: $rel"
    return 0
  fi

  if [[ -d "$src" ]]; then
    if [[ -d "$dst" && "$force" -eq 0 ]]; then
      log "Skip existing directory: $rel"
      return 0
    fi
    if [[ "$dry_run" -eq 1 ]]; then
      log "Would copy directory: $rel"
      return 0
    fi
    mkdir -p "$dst"
    cp -a "$src/." "$dst"
    log "Copied directory: $rel"
    return 0
  fi

  if [[ -e "$dst" && "$force" -eq 0 ]]; then
    log "Skip existing file: $rel"
    return 0
  fi

  if [[ "$dry_run" -eq 1 ]]; then
    log "Would copy file: $rel"
    return 0
  fi

  mkdir -p "$(dirname -- "$dst")"
  cp -a "$src" "$dst"
  log "Copied file: $rel"
}

write_template() {
  local rel="$1"
  local dst="$target_root/$rel"

  if [[ -e "$dst" && "$force" -eq 0 ]]; then
    log "Skip existing file: $rel"
    return 0
  fi

  if [[ "$dry_run" -eq 1 ]]; then
    log "Would write file: $rel"
    return 0
  fi

  mkdir -p "$(dirname -- "$dst")"
  cat > "$dst"
  log "Wrote file: $rel"
}

log "Bootstrapping workflow into: $target_root"

core_paths=(
  "AGENTS.md"
  "README.md"
  ".gitignore"
  "docs/agents.md"
  "docs/humans"
  "docs/workflow-audit.md"
  "docs/context-management.md"
  "docs/security.md"
  "docs/access-manifest.md"
  "docs/wiki/index.md"
  "docs/wiki/architecture-overview.md"
  "docs/wiki/playbooks"
  "docs/stacks"
  "skills/reasoning"
  "scripts/create-workflow-revision.sh"
  "scripts/bootstrap-workflow.sh"
  "scripts/validate-reasoning-skills.py"
  "docs/workflow-revisions.md"
)

for rel in "${core_paths[@]}"; do
  copy_path "$rel"
done

write_template "todo.md" <<'EOF'
# Todo

## Bugs

## Decision Queue

## Workflow Governance

## Current Focus

## Next Features & Updates

## Backlog
EOF

write_template "backlog.md" <<'EOF'
# Backlog
EOF

write_template "completed.md" <<'EOF'
# Completed Tasks
EOF

write_template "handover.md" <<'EOF'
# Handover

## Current Focus

## State Snapshot

## Recent Progress

## Next Steps

## Pending Items
EOF

write_template "CHANGELOG.md" <<'EOF'
# Changelog

Entries use ISO8601 timestamps and newest entries appear first.
EOF

write_template "todo-inbox.md" <<'EOF'
# Todo Inbox

## Bugs (triaged defects, regressions, or broken flows)
- Highest-priority defects that block users or break expected behavior.

## Decision Queue (non-blocking decisions collected during Continuous Mode)
- `Decision Needed: ...` items queued for user input after the continuous run finishes.

## Current Focus (highest priority)
- Bullet list of immediate tasks for the feature currently being developed/debugged.

## Next Features & Updates
- Bullet list of upcoming feature ideas and near-term improvements.

## Backlog
- Bullet list of lower-priority ideas for later consideration.
EOF

now_iso="$(date -Iseconds)"
write_template "docs/context/planner-task-manager.md" <<EOF
# Planner / Task Manager Ledger

## ${now_iso} — Workflow bootstrap
- Summary: Initialize workflow ledgers for this project.
- Details:
  - Replace this entry with the first real task.
- Related Spec / Skill: n/a
- Pending Actions: Start the first planned task.
- Status: open
EOF

if [[ "$dry_run" -eq 0 ]]; then
  mkdir -p "$target_root/docs/context/archive"
  mkdir -p "$target_root/specs"
fi

if [[ "$with_skills" -eq 1 ]]; then
  skill_paths=(
    "docs/skills"
    "skills/README.md"
    "skills/_schema"
    "skills/_template"
    "scripts/skillctl"
    "scripts/skillctl.py"
    "scripts/requirements-skillctl.txt"
    "scripts/setup-skillctl-venv.sh"
    "tests"
    "specs"
  )

  for rel in "${skill_paths[@]}"; do
    copy_path "$rel"
  done
fi

log "Bootstrap complete."
