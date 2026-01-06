#!/usr/bin/env bash
set -euo pipefail

ROOT="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"

if [[ ! -f "$ROOT/arbitration/arbitrator.js" ]]; then
  echo "Arbitration engine not found: $ROOT/arbitration/arbitrator.js" >&2
  exit 1
fi

if ! command -v node >/dev/null 2>&1; then
  echo "Node.js is required to run arbitration validation." >&2
  exit 1
fi

INPUT=""
if [[ -n "${ARBITRATION_INPUT:-}" && -f "$ARBITRATION_INPUT" ]]; then
  INPUT="$ARBITRATION_INPUT"
else
  for candidate in \
    "logs/planner-output.json" \
    "logs/task-plan.json" \
    "artifacts/planner-output.json" \
    "artifacts/task-plan.json" \
    "planner-output.json" \
    "task-plan.json"; do
    if [[ -f "$ROOT/$candidate" ]]; then
      INPUT="$ROOT/$candidate"
      break
    fi
  done
fi

if [[ -z "$INPUT" ]]; then
  INPUT="$ROOT/templates/arbitration/fixture.json"
fi

if [[ ! -f "$INPUT" ]]; then
  echo "Arbitration input not found: $INPUT" >&2
  exit 1
fi

mkdir -p "$ROOT/logs"
OUT_PRIMARY="$ROOT/logs/arbitration-decision.json"
OUT_SECOND="$ROOT/logs/arbitration-decision-second.json"

node "$ROOT/arbitration/arbitrator.js" --input "$INPUT" --output "$OUT_PRIMARY"
node "$ROOT/arbitration/arbitrator.js" --input "$INPUT" --output "$OUT_SECOND"

node - <<'NODE' "$OUT_PRIMARY" "$OUT_SECOND"
const fs = require('node:fs');

function stableStringify(value) {
  if (Array.isArray(value)) {
    return `[${value.map((item) => stableStringify(item)).join(',')}]`;
  }
  if (value && typeof value === 'object') {
    const keys = Object.keys(value).sort();
    return `{${keys.map((key) => `${JSON.stringify(key)}:${stableStringify(value[key])}`).join(',')}}`;
  }
  return JSON.stringify(value);
}

function sanitize(obj) {
  const clone = JSON.parse(JSON.stringify(obj));
  if (clone.decision_log) {
    delete clone.decision_log.generated_at;
  }
  return clone;
}

const [fileA, fileB] = process.argv.slice(2);
const outputA = JSON.parse(fs.readFileSync(fileA, 'utf8'));
const outputB = JSON.parse(fs.readFileSync(fileB, 'utf8'));

if (outputA.status !== 'ok') {
  console.error(`Arbitration failed: status=${outputA.status}`);
  if (Array.isArray(outputA.blocked) && outputA.blocked.length) {
    console.error(`Blocked tasks: ${outputA.blocked.map((item) => item.task_id).join(', ')}`);
  }
  process.exit(1);
}

const sanitizedA = sanitize(outputA);
const sanitizedB = sanitize(outputB);

const hashA = stableStringify(sanitizedA);
const hashB = stableStringify(sanitizedB);

if (hashA !== hashB) {
  console.error('Determinism check failed: arbitration outputs differ between runs.');
  process.exit(1);
}
NODE

cat "$OUT_PRIMARY"
