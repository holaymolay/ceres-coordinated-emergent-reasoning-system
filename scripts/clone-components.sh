#!/usr/bin/env bash
set -euo pipefail

# Clone missing CERES component repos defined in repos.yaml.
# Usage: ./scripts/clone-components.sh [--org <github_org>]

ORG="holaymolay"
if [[ "${1:-}" == "--org" && -n "${2:-}" ]]; then
  ORG="$2"
fi

REPOS_FILE="$(dirname "$0")/../repos.yaml"
if [[ ! -f "$REPOS_FILE" ]]; then
  echo "repos.yaml not found at $REPOS_FILE" >&2
  exit 1
fi

parse_pairs() {
  awk '
    /^- name:/ { name=$3 }
    /local_path:/ { path=$2; print name "|" path }
  ' "$REPOS_FILE"
}

while IFS='|' read -r NAME PATH; do
  [[ -z "$NAME" || -z "$PATH" ]] && continue
  if [[ -d "$PATH/.git" ]]; then
    echo "✔ $PATH already exists"
    continue
  fi
  REMOTE="https://github.com/${ORG}/${NAME}.git"
  echo "Cloning $NAME into $PATH from $REMOTE ..."
  git clone "$REMOTE" "$PATH"
done < <(parse_pairs)
