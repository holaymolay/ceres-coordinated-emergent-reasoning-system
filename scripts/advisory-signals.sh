#!/usr/bin/env bash
set -euo pipefail

# Advisory Concept/Synchronization signal scaffold (non-binding).
# Usage: ./scripts/advisory-signals.sh [specs/elicitation/<spec-id>.md]

ELICITATION="${1:-specs/elicitation/elicitation.md}"

if [[ -f "$ELICITATION" ]]; then
  echo "Reading signals from $ELICITATION ..." >&2
fi

cat <<'TEMPLATE'
## Concept Signals (Advisory)
- Candidate Concept A (reason)
- Candidate Concept B (reason)

## Synchronization Signals (Advisory)
- Concept A ↔ Concept B (why)
TEMPLATE
