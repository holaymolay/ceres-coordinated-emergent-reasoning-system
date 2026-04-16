#!/usr/bin/env bash
set -euo pipefail

# Resolver scaffold: list answerable_by_system gaps that are unresolved.
# Expects a Gap Ledger JSON/YAML with fields defined in the CERES hub schemas.

GAP_LEDGER="${1:-gap-ledger.json}"

if [[ ! -f "$GAP_LEDGER" ]]; then
  echo "Gap ledger not found: $GAP_LEDGER" >&2
  exit 1
fi

if ! command -v jq >/dev/null 2>&1; then
  echo "jq required for resolver loop" >&2
  exit 1
fi

IDS=($(jq -r '.gaps[] | select(.answerable_by_system==true and .status!="resolved") | .gap_id' "$GAP_LEDGER" 2>/dev/null))

if [[ ${#IDS[@]} -eq 0 ]]; then
  echo "No answerable_by_system gaps to resolve."
  exit 0
fi

echo "Answerable_by_system gaps (unresolved):"
for id in "${IDS[@]}"; do
  echo "- $id"
done

echo
echo "Resolve each with evidence (file/line, command output, tests) and update the Gap Ledger. Then run scripts/validate-gap-ledger.py."
