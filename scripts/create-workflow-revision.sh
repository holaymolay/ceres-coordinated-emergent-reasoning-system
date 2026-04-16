#!/usr/bin/env bash
set -euo pipefail

repo_root="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
revisions_dir="$repo_root/ai_workflow_revisions"

mkdir -p "$revisions_dir"

current_dirs=()
while IFS= read -r -d '' dir; do
  current_dirs+=("$dir")
done < <(find "$revisions_dir" -maxdepth 1 -type d -name 'rev_*_current' -print0)

if (( ${#current_dirs[@]} > 1 )); then
  printf 'Error: multiple *_current revisions found:\n' >&2
  printf '  - %s\n' "${current_dirs[@]##*/}" >&2
  exit 1
fi

max_rev=0
while IFS= read -r -d '' dir; do
  base="${dir##*/}"             # rev_008_current
  num="${base#rev_}"            # 008_current
  num="${num%_current}"         # 008
  if [[ "$num" =~ ^[0-9]{3}$ ]]; then
    val=$((10#$num))
    if (( val > max_rev )); then
      max_rev="$val"
    fi
  fi
done < <(find "$revisions_dir" -maxdepth 1 -type d -name 'rev_*' -print0)

next_rev=$((max_rev + 1))
next_rev_padded="$(printf '%03d' "$next_rev")"
new_dir="$revisions_dir/rev_${next_rev_padded}_current"

if (( ${#current_dirs[@]} == 1 )); then
  current_dir="${current_dirs[0]}"
  current_base="${current_dir##*/}"           # rev_008_current
  previous_dir="$revisions_dir/${current_base%_current}" # rev_008

  if [[ -e "$previous_dir" ]]; then
    printf 'Error: expected %s to not exist (cannot rename current revision)\n' "$previous_dir" >&2
    exit 1
  fi

  mv "$current_dir" "$previous_dir"
fi

mkdir -p "$new_dir"

copy_path() {
  local rel="$1"
  local src="$repo_root/$rel"
  local dst="$new_dir/$rel"

  if [[ ! -e "$src" ]]; then
    printf 'Warning: skipping missing path: %s\n' "$rel" >&2
    return 0
  fi

  mkdir -p "$(dirname -- "$dst")"
  if [[ -d "$src" ]]; then
    cp -a "$src" "$dst"
  else
    cp -a "$src" "$dst"
  fi
}

paths=(
  "AGENTS.md"
  "README.md"
  "HUMAN_START_HERE.md"
  ".gitignore"
  "docs/workflow-revisions.md"
  "todo-inbox.md"
  "todo.md"
  "backlog.md"
  "completed.md"
  "handover.md"
  "CHANGELOG.md"

  "docs/agents.md"
  "docs/humans"
  "docs/workflow-audit.md"
  "docs/context-management.md"
  "docs/security.md"
  "docs/access-manifest.md"
  "docs/prompts"
  "docs/context"
  "docs/wiki/index.md"
  "docs/wiki/architecture-overview.md"
  "docs/wiki/playbooks"
  "docs/stacks"

  "docs/skills"
  "skills/README.md"
  "skills/_schema"
  "skills/_template"
  "skills/reasoning"
  "specs"

  "scripts"
  "tests"
)

for rel in "${paths[@]}"; do
  copy_path "$rel"
done

printf 'Created workflow revision: %s\n' "${new_dir##*/}"
