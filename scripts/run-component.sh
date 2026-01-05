#!/usr/bin/env bash
set -euo pipefail

# Run a command inside a CERES component repo.
# Usage: ./scripts/run-component.sh <component-name> "<command>"

if [[ $# -lt 2 ]]; then
  echo "Usage: $0 <component-name> \"<command>\"" >&2
  exit 1
fi

COMPONENT="$1"
shift
CMD="$*"

REPOS_FILE="$(dirname "$0")/../repos.yaml"
PATH_DIR=""
while IFS='|' read -r NAME PATH; do
  [[ "$NAME" == "$COMPONENT" ]] && PATH_DIR="$PATH"
done < <(awk '/^- name:/ {name=$3} /local_path:/ {path=$2; print name "|" path}' "$REPOS_FILE")

if [[ -z "$PATH_DIR" ]]; then
  echo "Component $COMPONENT not found in repos.yaml" >&2
  exit 1
fi

if [[ ! -d "$PATH_DIR/.git" ]]; then
  echo "Component $COMPONENT not present locally at $PATH_DIR; run ./scripts/clone-components.sh first." >&2
  exit 1
fi

( cd "$PATH_DIR" && eval "$CMD" )
