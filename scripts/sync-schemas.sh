#!/usr/bin/env bash
set -euo pipefail

# Sync hub schemas into a target repository's schemas/ directory.
# Usage: ./scripts/sync-schemas.sh <target-dir>

TARGET="${1:-}"
if [[ -z "$TARGET" ]]; then
  echo "Usage: $0 <target-dir>" >&2
  exit 1
fi

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SRC="$ROOT/schemas"
DEST="$TARGET/schemas"

if [[ ! -d "$SRC" ]]; then
  echo "Schema source not found: $SRC" >&2
  exit 1
fi

mkdir -p "$DEST"
cp "$SRC"/*.schema.json "$DEST"/

echo "Synced schemas to $DEST"
