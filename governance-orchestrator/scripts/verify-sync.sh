#!/usr/bin/env bash
set -euo pipefail

repo_root="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo_root"

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "ERROR: Not inside a git repository." >&2
  exit 1
fi

if [[ -n "$(git status --porcelain)" ]]; then
  echo "ERROR: Working tree is dirty. Commit or stash changes before wrap-up." >&2
  exit 1
fi

branch="$(git rev-parse --abbrev-ref HEAD)"
if [[ "$branch" == "HEAD" ]]; then
  echo "ERROR: Detached HEAD; cannot verify push state." >&2
  exit 1
fi

upstream="$(git rev-parse --abbrev-ref --symbolic-full-name "@{u}" 2>/dev/null || true)"
if [[ -z "$upstream" ]]; then
  echo "ERROR: No upstream configured for ${branch}. Push with \`git push --set-upstream origin ${branch}\` before finishing the task." >&2
  exit 1
fi

remote="${upstream%%/*}"
remote="${remote:-origin}"

if ! git fetch --quiet "$remote"; then
  echo "ERROR: Failed to fetch from ${remote}. Resolve network/auth issues before wrap-up." >&2
  exit 1
fi

counts="$(git rev-list --left-right --count HEAD..."${upstream}")"
ahead="$(echo "$counts" | awk '{print $1}')"
behind="$(echo "$counts" | awk '{print $2}')"

if [[ "$ahead" -gt 0 && "$behind" -gt 0 ]]; then
  echo "ERROR: Branch ${branch} has diverged from ${upstream} (ahead ${ahead}, behind ${behind}). Reconcile and push." >&2
  exit 1
elif [[ "$ahead" -gt 0 ]]; then
  echo "ERROR: Branch ${branch} is ahead of ${upstream} by ${ahead} commit(s); push before closing the task." >&2
  exit 1
elif [[ "$behind" -gt 0 ]]; then
  echo "ERROR: Branch ${branch} is behind ${upstream} by ${behind} commit(s); pull/rebase and push before closing the task." >&2
  exit 1
fi

echo "OK: ${branch} is in sync with ${upstream}."
