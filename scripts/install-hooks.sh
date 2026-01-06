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

# Auto-export handover when memory changes.
if [[ -f "memory.md" ]]; then
  if git diff --name-only --cached | grep -q "^memory\.md$" || git diff --name-only | grep -q "^memory\.md$"; then
    ./scripts/export-handover.py
    git add handover.md
  fi
fi

# CERES single-concept enforcement (staged files only).
# Concepts live under concepts/<concept_name>/.
# Commits may touch exactly one Concept, or only allowed metadata files.

allowed_non_concept() {
  local file="$1"
  case "$file" in
    README.md|README.*|.gitignore|LICENSE|LICENSE.*|NOTICE|NOTICE.*|CONSTITUTION.md|PROMPTLOADER.md|memory.md|handover.md|todo.md|todo-inbox.md|completed.md)
      return 0
      ;;
    docs/*|scripts/*|templates/*|schemas/*|prompt-debugger/*|arbitration/*|planner/*|.github/*)
      return 0
      ;;
    *)
      return 1
      ;;
  esac
}

staged_files=()
while IFS= read -r file; do
  staged_files+=("$file")
done < <(git diff --cached --name-only --diff-filter=ACMRT)

if [[ ${#staged_files[@]} -eq 0 ]]; then
  exit 0
fi

concepts=()
non_concept=()

for file in "${staged_files[@]}"; do
  if [[ "$file" == concepts/*/* ]]; then
    concept="${file#concepts/}"
    concept="${concept%%/*}"
    concepts+=("$concept")
  elif allowed_non_concept "$file"; then
    :
  else
    non_concept+=("$file")
  fi
done

# Deduplicate concept list.
unique_concepts=($(printf '%s
' "${concepts[@]}" | awk '!seen[$0]++'))

if [[ ${#unique_concepts[@]} -gt 1 ]]; then
  echo "ERROR: CERES single-Concept commit enforced." >&2
  echo "Detected Concepts: ${unique_concepts[*]}" >&2
  echo "Fix: split changes into separate commits per Concept." >&2
  exit 1
fi

if [[ ${#unique_concepts[@]} -eq 0 && ${#non_concept[@]} -gt 0 ]]; then
  echo "ERROR: No Concept changes detected and non-metadata files were staged." >&2
  echo "Non-Concept files: ${non_concept[*]}" >&2
  echo "Fix: move changes under concepts/<name>/ or restrict to allowed metadata files." >&2
  exit 1
fi

if [[ ${#unique_concepts[@]} -eq 1 && ${#non_concept[@]} -gt 0 ]]; then
  echo "ERROR: Non-Concept files staged alongside Concept '${unique_concepts[0]}'." >&2
  echo "Non-Concept files: ${non_concept[*]}" >&2
  echo "Fix: keep non-Concept files to allowed metadata only, or split the commit." >&2
  exit 1
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
