#!/usr/bin/env bash
set -euo pipefail

# Initialize CERES todo artifacts in a target directory (default: current directory).
# Usage: ./scripts/init-todo-files.sh [target-dir]

TARGET_DIR="${1:-.}"
TEMPLATE_DIR="$(dirname "$0")/../templates/todo"

if [[ ! -d "$TEMPLATE_DIR" ]]; then
  echo "Template directory not found: $TEMPLATE_DIR" >&2
  exit 1
fi

mkdir -p "$TARGET_DIR"

copy_file() {
  local src="$1"
  local dest="$2"
  if [[ -e "$dest" ]]; then
    echo "Skipping existing $dest"
  else
    cp "$src" "$dest"
    echo "Created $dest"
  fi
}

copy_file "$TEMPLATE_DIR/todo-inbox.md" "$TARGET_DIR/todo-inbox.md"
copy_file "$TEMPLATE_DIR/todo.md" "$TARGET_DIR/todo.md"
copy_file "$TEMPLATE_DIR/completed.md" "$TARGET_DIR/completed.md"
copy_file "$TEMPLATE_DIR/handover.md" "$TARGET_DIR/handover.md"
