#!/usr/bin/env bash
set -euo pipefail

repo_root="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo_root"

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "Auto-push skipped: not a git repository."
  exit 0
fi

if [[ -n "$(git status --porcelain)" ]]; then
  echo "Auto-push skipped: working tree not clean (commit or stash first)."
  exit 0
fi

branch="$(git rev-parse --abbrev-ref HEAD)"
if [[ "$branch" == "HEAD" ]]; then
  echo "Auto-push skipped: detached HEAD."
  exit 0
fi

upstream="$(git rev-parse --abbrev-ref --symbolic-full-name "@{u}" 2>/dev/null || true)"
if [[ -z "$upstream" ]]; then
  echo "Auto-push skipped: no upstream configured for ${branch}."
  exit 0
fi

commit_msg="$(git log -1 --pretty=%B)"
if echo "$commit_msg" | grep -Eqi "\b(wip|draft|tmp|temp|partial|half-baked|incomplete)\b|do not push"; then
  echo "Auto-push skipped: commit message indicates WIP or incomplete work."
  exit 0
fi

if ! command -v rg >/dev/null 2>&1; then
  echo "Auto-push skipped: ripgrep (rg) not available for secret scan."
  exit 0
fi

if git rev-parse --verify HEAD^ >/dev/null 2>&1; then
  numstat_cmd=(git diff --numstat HEAD^ HEAD)
else
  numstat_cmd=(git diff --numstat --root HEAD)
fi

mapfile -t changed_files < <("${numstat_cmd[@]}" | awk '($1 != "-" && $2 != "-") {print $3}')

if [[ ${#changed_files[@]} -eq 0 ]]; then
  echo "Auto-push skipped: no text files detected in last commit."
  exit 0
fi


is_env_template() {
  local file="$1"
  case "$file" in
    .env.example|.env.template|.env.sample|.env.dist|env.example|env.template|env.sample|env.dist|*.env.example|*.env.template|*.env.sample|*.env.dist)
      return 0
      ;;
    *)
      return 1
      ;;
  esac
}

patterns=(
  'AKIA[0-9A-Z]{16}'
  'ASIA[0-9A-Z]{16}'
  'AIza[0-9A-Za-z_-]{35}'
  'ghp_[A-Za-z0-9]{36}'
  'github_pat_[A-Za-z0-9_]{10,}'
  'xox[baprs]-[0-9A-Za-z-]{10,}'
  'sk-[A-Za-z0-9]{32,}'
  '-----BEGIN (RSA|EC|OPENSSH|PRIVATE) KEY-----'
)


scan_files=()
for file in "${changed_files[@]}"; do
  if is_env_template "$file"; then
    continue
  fi
  scan_files+=("$file")
done

for pattern in "${patterns[@]}"; do
  if [[ ${#scan_files[@]} -gt 0 ]] && rg --no-messages -n -e "$pattern" -- "${scan_files[@]}"; then
    echo "Auto-push skipped: potential secret pattern matched ($pattern)."
    exit 0
  fi
done

if ! git push; then
  echo "Auto-push failed: git push returned non-zero." >&2
  exit 0
fi

if ! "$repo_root/scripts/verify-sync.sh" >/dev/null 2>&1; then
  echo "Auto-push warning: verify-sync failed after push." >&2
  exit 0
fi

echo "Auto-push succeeded."
