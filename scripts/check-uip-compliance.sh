#!/usr/bin/env bash
set -euo pipefail

report_violation() {
  local category="$1"
  local file="$2"
  local rule="$3"
  local suggestion="$4"
  echo "${category} | file: ${file} | rule: ${rule} | suggestion: ${suggestion}" >&2
  exit 1
}

MARKUP_GLOB="*.{ts,tsx,js,jsx}"
IMPORT_GLOB="*.{ts,tsx,js,jsx,py}"

SCAN_EXCLUDES=(
  --glob '!concepts/**/adapter/**'
  --glob '!ui-adapters/**'
  --glob '!renderer/**'
  --glob '!renderers/**'
  --glob '!ui-patterns/**'
)
BOUNDARY_EXCLUDES=()

scan_forbidden() {
  local pattern="$1"
  local label="$2"
  local targets=(concepts skills)
  if [[ -d agents ]]; then
    targets+=(agents)
  fi
  local matches
  matches=$(rg -n -m1 "$pattern" "${targets[@]}" "${SCAN_EXCLUDES[@]}" --glob "$MARKUP_GLOB" || true)
  if [[ -n "$matches" ]]; then
    local file="${matches%%:*}"
    report_violation \
      "UIP-BOUNDARY-VIOLATION" \
      "$file" \
      "UIP violation: UI markup or styling detected outside adapter layer (${label})" \
      "Move UI markup/styling into ui-adapters/ or renderer/ allowlisted paths."
  fi
}

check_imports() {
  local target="$1"
  local pattern="$2"
  local rule="$3"
  local suggestion="$4"
  if [[ -d "$target" ]]; then
    local matches
    matches=$(rg -n -m1 "$pattern" "$target" "${BOUNDARY_EXCLUDES[@]}" --glob "$IMPORT_GLOB" || true)
    if [[ -n "$matches" ]]; then
      local file="${matches%%:*}"
      report_violation "UIP-BOUNDARY-VIOLATION" "$file" "$rule" "$suggestion"
    fi
  fi
}

scan_forbidden '<div' 'HTML/JSX <div'
scan_forbidden '<button' 'HTML/JSX <button'
scan_forbidden '<form' 'HTML/JSX <form'
scan_forbidden '<input' 'HTML/JSX <input'
scan_forbidden '<select' 'HTML/JSX <select'
scan_forbidden 'className=' 'className usage'
scan_forbidden '\\b(bg|text|flex|grid|px|py|mx|my|mt|mb|ml|mr|pt|pb|pl|pr|w|h)-[a-z0-9-]+' 'Tailwind class patterns'
scan_forbidden 'tailwind' 'Tailwind keyword'

# Schema-aware enforcement (runs after blunt scan)
scripts_dir="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
"${scripts_dir}/check-uip-schemas.py"

# Directional dependency enforcement
check_imports \
  "agents" \
  "ui-adapters/|renderer/|renderers/|ui-patterns/" \
  "UIP violation: agent importing adapter layer" \
  "Remove adapter/renderer imports from agents and emit UI intent instead."

check_imports \
  "skills" \
  "ui-adapters/|renderer/|renderers/|ui-patterns/" \
  "UIP violation: skill importing adapter layer" \
  "Remove adapter/renderer imports from skills and emit UI intent instead."

check_imports \
  "skills" \
  "from ['\"]react['\"]|require\\(['\"]react['\"]\\)" \
  "UIP violation: skill importing React" \
  "Remove React imports from skills; keep rendering in adapter layers."

check_imports \
  "skills" \
  "from ['\"](tailwind|tailwindcss)['\"]|require\\(['\"](tailwind|tailwindcss)['\"]\\)" \
  "UIP violation: skill importing Tailwind" \
  "Remove Tailwind imports from skills; keep styling in adapter layers."

for dir in renderer renderers; do
  check_imports \
    "$dir" \
    "concepts/|agents/|skills/" \
    "UIP violation: renderer importing domain layer" \
    "Remove concept/agent/skill imports from renderers and consume intent artifacts only."
done

exit 0
