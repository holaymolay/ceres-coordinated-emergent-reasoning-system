#!/usr/bin/env bash
set -euo pipefail

# Initialize CERES governance artifacts in a target directory (default: current directory).
# Usage: ./scripts/init-artifacts.sh [target-dir]

TARGET_DIR="${1:-.}"
TEMPLATE_DIR="$(dirname "$0")/../templates/artifacts"

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

copy_file "$TEMPLATE_DIR/objective-contract.json" "$TARGET_DIR/objective-contract.json"
copy_file "$TEMPLATE_DIR/gap-ledger.json" "$TARGET_DIR/gap-ledger.json"
