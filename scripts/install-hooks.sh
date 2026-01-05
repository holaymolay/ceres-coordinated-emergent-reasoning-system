#!/usr/bin/env bash
set -euo pipefail

HOOK_DIR="$(git rev-parse --git-path hooks)"
HOOK_PATH="$HOOK_DIR/pre-commit"
TIMESTAMP="$(date +%Y%m%d%H%M%S)"

mkdir -p "$HOOK_DIR"

if [[ -e "$HOOK_PATH" ]]; then
  cp "$HOOK_PATH" "${HOOK_PATH}.ceres.bak.${TIMESTAMP}"
fi

cat > "$HOOK_PATH" <<'HOOK'
#!/usr/bin/env bash
set -euo pipefail

if [[ -f "memory.md" ]]; then
  if git diff --name-only --cached | grep -q "^memory\.md$" || git diff --name-only | grep -q "^memory\.md$"; then
    ./scripts/export-handover.py
    git add handover.md
  fi
fi
HOOK

chmod +x "$HOOK_PATH"


POST_COMMIT_PATH="$HOOK_DIR/post-commit"

if [[ -e "$POST_COMMIT_PATH" ]]; then
  cp "$POST_COMMIT_PATH" "${POST_COMMIT_PATH}.ceres.bak.${TIMESTAMP}"
fi

cat > "$POST_COMMIT_PATH" <<'HOOK'
#!/usr/bin/env bash
set -euo pipefail

if [[ -x "./scripts/auto-push-if-safe.sh" ]]; then
  ./scripts/auto-push-if-safe.sh
fi

if [[ -x "./scripts/git-hooks/post-commit-push-check.sh" ]]; then
  ./scripts/git-hooks/post-commit-push-check.sh
fi
HOOK

chmod +x "$POST_COMMIT_PATH"
echo "Installed CERES hooks: pre-commit handover export + post-commit auto-push + push check."
