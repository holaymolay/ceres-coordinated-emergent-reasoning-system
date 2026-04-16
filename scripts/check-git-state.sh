#!/usr/bin/env bash
set -euo pipefail

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "ERROR: Not inside a git repository." >&2
  exit 1
fi

if [[ -n "$(git status --porcelain)" ]]; then
  echo "ERROR: Working tree is dirty. Commit or stash changes before starting a new task." >&2
  exit 1
fi

remote_branch=$(git symbolic-ref --quiet --short refs/remotes/origin/HEAD | sed 's@^origin/@@')
remote_branch=${remote_branch:-master}

git fetch origin "$remote_branch" >/dev/null 2>&1

counts=$(git rev-list --left-right --count "origin/${remote_branch}...HEAD" || echo "0 0")
behind=$(echo "$counts" | awk '{print $1}')

if [[ "$behind" -gt 0 ]]; then
  echo "ERROR: Local branch is behind origin/${remote_branch}. Pull/rebase before starting new work." >&2
  exit 1
fi

exit 0
