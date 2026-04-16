#!/usr/bin/env bash
set -euo pipefail

# Interrogation loop scaffold: ask one bounded question per blocking gap.
# Expects a Gap Ledger JSON/YAML with fields defined in the CERES hub schemas.

GAP_LEDGER="${1:-gap-ledger.json}"

if [[ ! -f "$GAP_LEDGER" ]]; then
  echo "Gap ledger not found: $GAP_LEDGER" >&2
  exit 1
fi

if ! command -v jq >/dev/null 2>&1; then
  echo "jq required for interrogation loop" >&2
  exit 1
fi

BLOCKING_IDS=($(jq -r '.gaps[] | select(.blocking==true and .status!="resolved") | .gap_id' "$GAP_LEDGER" 2>/dev/null))

if [[ ${#BLOCKING_IDS[@]} -eq 0 ]]; then
  echo "No blocking gaps to interrogate."
  exit 0
fi

echo "Blocking gaps (unresolved):"
for id in "${BLOCKING_IDS[@]}"; do
  echo "- $id"
done

echo
echo "Ask ONE bounded question for the next gap, record the answer/evidence in the Gap Ledger, then rerun validation (scripts/validate-gap-ledger.py)."
