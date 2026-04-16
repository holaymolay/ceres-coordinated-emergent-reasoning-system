#!/usr/bin/env bash
set -euo pipefail

profile="${EXECUTION_PROFILE:-SAFE}"
if [[ "$profile" != "SAFE" && "$profile" != "FAST" ]]; then
  echo "ERROR: EXECUTION_PROFILE must be SAFE or FAST (got '$profile')." >&2
  exit 1
fi

get_changed_files() {
  local staged unstaged untracked
  if [[ -n "${GITHUB_ACTIONS:-}" && -n "${GITHUB_BASE_REF:-}" ]]; then
    git fetch origin "${GITHUB_BASE_REF}" --depth=1 >/dev/null 2>&1 || true
    git diff --name-only "origin/${GITHUB_BASE_REF}...HEAD" | sed '/^$/d' | sort -u
    return
  fi
  staged=$(git diff --name-only --cached || true)
  unstaged=$(git diff --name-only || true)
  untracked=$(git ls-files --others --exclude-standard || true)
  printf "%s\n" "$staged" "$unstaged" "$untracked" | sed '/^$/d' | sort -u
}

changed_files=$(get_changed_files)

fast_scope="${FAST_MODE_SCOPE:-}"
if [[ "$profile" == "FAST" ]]; then
  if [[ -z "$fast_scope" ]]; then
    echo "ERROR: Fast Mode requires FAST_MODE_SCOPE to be set." >&2
    exit 1
  fi
  if ! grep -q 'Fast Mode' handover.md || ! grep -q "$fast_scope" handover.md; then
    echo "ERROR: Fast Mode must be logged in handover.md with the active scope." >&2
    exit 1
  fi
  if ! grep -q 'Fast Mode' docs/context/planner-task-manager.md || ! grep -q "$fast_scope" docs/context/planner-task-manager.md; then
    echo "ERROR: Fast Mode scope must be recorded in the planner ledger." >&2
    exit 1
  fi
  if ! grep -q "$fast_scope" todo.md; then
    echo "ERROR: Fast Mode scope is no longer active in todo.md; Fast Mode must expire." >&2
    exit 1
  fi
  if grep -q '^synchronizations/' <<< "$changed_files"; then
    echo "ERROR: Fast Mode cannot be active during Synchronization changes." >&2
    exit 1
  fi
  security_sensitive=false
  while IFS= read -r file; do
    case "$file" in
      docs/security.md|docs/access-manifest.md)
        security_sensitive=true
        ;;
      specs/*auth*|specs/*security*)
        security_sensitive=true
        ;;
      concepts/*/auth*|concepts/*/security*)
        security_sensitive=true
        ;;
      skills/*/auth*|skills/*/security*)
        security_sensitive=true
        ;;
    esac
  done <<< "$changed_files"
  if [[ "$security_sensitive" == "true" ]]; then
    echo "ERROR: Fast Mode cannot be active during security-sensitive changes." >&2
    exit 1
  fi
fi

concepts=()
while IFS= read -r file; do
  if [[ "$file" == concepts/*/* ]]; then
    concept=${file#concepts/}
    concept=${concept%%/*}
    if [[ ! " ${concepts[*]} " =~ " ${concept} " ]]; then
      concepts+=("$concept")
    fi
  fi
done <<< "$changed_files"

if (( ${#concepts[@]} > 1 )); then
  if ! grep -q '^synchronizations/' <<< "$changed_files"; then
    echo "ERROR: Cross-Concept changes require a Synchronization under /synchronizations/." >&2
  fi
  echo "ERROR: One-Concept-per-commit violation. Multiple Concepts changed: ${concepts[*]}" >&2
  exit 1
fi

code_changes=false
while IFS= read -r file; do
  if [[ "$file" == docs/* ]]; then
    continue
  fi
  case "$file" in
    completed.md|handover.md|CHANGELOG.md|todo.md|todo-inbox.md|backlog.md)
      continue
      ;;
  esac
  code_changes=true
  break
fi <<< "$changed_files"

if [[ "$code_changes" == "true" ]]; then
  if ! grep -q '^completed.md$' <<< "$changed_files"; then
    echo "ERROR: completed.md must be updated when code changes exist." >&2
    exit 1
  fi
  if ! grep -q '^handover.md$' <<< "$changed_files"; then
    echo "ERROR: handover.md must be updated when code changes exist." >&2
    exit 1
  fi
  if [[ "$profile" == "SAFE" ]]; then
    if ! grep -q '^CHANGELOG.md$' <<< "$changed_files"; then
      echo "ERROR: CHANGELOG.md must be updated in SAFE mode when code changes exist." >&2
      exit 1
    fi
    if ! grep -q '^runs/.\+/[^/]*\.jsonl$' <<< "$changed_files"; then
      echo "ERROR: Run record required in SAFE mode (runs/YYYY-MM-DD/<run-id>.jsonl)." >&2
      exit 1
    fi
  fi
fi

workflow_request=false
if [[ -f todo-inbox.md ]]; then
  while IFS= read -r line; do
    if [[ "$line" =~ ^-\  ]]; then
      if [[ "$line" == *"Bullet list"* || "$line" == *"Highest-priority"* || "$line" == *"Decision Needed"* ]]; then
        continue
      fi
      if grep -qiE 'AGENTS\.md|docs/agents\.md|workflow|governance|context-management|context management' <<< "$line"; then
        workflow_request=true
        break
      fi
    fi
  done < todo-inbox.md
fi

if [[ "$workflow_request" == "true" ]]; then
  if ! awk '/^## Workflow Governance/{flag=1;next}/^## /{flag=0}flag && /^- \[ \]/{found=1}END{exit !found}' todo.md; then
    echo "ERROR: Workflow-related inbox items must be promoted to ## Workflow Governance in todo.md." >&2
    exit 1
  fi
fi

exit 0
