#!/usr/bin/env bash
set -euo pipefail

ROOT="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"

if command -v python3 >/dev/null 2>&1; then
  if [[ -f "$ROOT/scripts/validate-arbitration-ci.py" ]]; then
    python3 "$ROOT/scripts/validate-arbitration-ci.py" "$@" && exit 0
    echo "WARN: Python fallback failed; continuing with shell logic." >&2
  fi
fi

if [[ ! -f "$ROOT/arbitration/arbitrator.js" ]]; then
  echo "Arbitration engine not found: $ROOT/arbitration/arbitrator.js" >&2
  exit 1
fi

if ! command -v node >/dev/null 2>&1; then
  echo "Node.js is required to run arbitration validation." >&2
  exit 1
fi

planner_dir=""

has_planner_files() {
  local dir="$1"
  [[ -f "$dir/task_graph.json" && -f "$dir/concept_map.json" && -f "$dir/required_syncs.json" ]]
}

should_exclude_path() {
  local file="$1"
  if [[ "$file" == *"/.git/"* || "$file" == *"/node_modules/"* ]]; then
    return 0
  fi
  local exclude
  for exclude in "${EXCLUDES[@]}"; do
    if [[ -n "$exclude" && "$file" == *"/$exclude/"* ]]; then
      return 0
    fi
  done
  return 1
}

EXCLUDES=()
if [[ -f "$ROOT/repos.yaml" ]]; then
  while read -r value; do
    EXCLUDES+=("$value")
  done < <(awk '/local_path:/{print $2}' "$ROOT/repos.yaml")
fi

if [[ -n "${ARBITRATION_PLANNER_DIR:-}" ]]; then
  candidate="$(cd "$(dirname "$ARBITRATION_PLANNER_DIR")" && pwd)/$(basename "$ARBITRATION_PLANNER_DIR")"
  if [[ ! -d "$candidate" ]]; then
    echo "ARBITRATION_PLANNER_DIR is not a directory: $ARBITRATION_PLANNER_DIR" >&2
    exit 1
  fi
  if ! has_planner_files "$candidate"; then
    echo "ARBITRATION_PLANNER_DIR missing required planner artifacts: $candidate" >&2
    exit 1
  fi
  planner_dir="$candidate"
else
  candidates=()
  while IFS= read -r -d '' file; do
    if should_exclude_path "$file"; then
      continue
    fi
    dir="$(dirname "$file")"
    if has_planner_files "$dir"; then
      candidates+=("$dir")
    fi
  done < <(find "$ROOT" -type f -name "task_graph.json" -print0)

  if [[ ${#candidates[@]} -gt 0 ]]; then
    mapfile -t unique_candidates < <(printf '%s\n' "${candidates[@]}" | sort -u)
    if [[ ${#unique_candidates[@]} -gt 1 ]]; then
      echo "Multiple planner output directories detected; set ARBITRATION_PLANNER_DIR to disambiguate:" >&2
      printf '  - %s\n' "${unique_candidates[@]}" >&2
      exit 1
    fi
    planner_dir="${unique_candidates[0]}"
  fi
fi

mkdir -p "$ROOT/logs"
OUT_PRIMARY="$ROOT/logs/arbitration-decision.json"
OUT_SECOND="$ROOT/logs/arbitration-decision-second.json"
INPUT=""

if [[ -n "$planner_dir" ]]; then
  if [[ ! -f "$ROOT/planner/planner-output-validator.js" ]]; then
    echo "Planner output validator not found: $ROOT/planner/planner-output-validator.js" >&2
    exit 1
  fi

  echo "Planner output detected: $planner_dir"
  node "$ROOT/planner/planner-output-validator.js" --dir "$planner_dir"

  INPUT="$ROOT/logs/arbitration-input.json"
  node - <<'NODE' "$planner_dir" "$INPUT"
const fs = require('node:fs');
const path = require('node:path');

const [dir, outPath] = process.argv.slice(2);

function readJson(name) {
  return JSON.parse(fs.readFileSync(path.join(dir, name), 'utf8'));
}

const taskGraph = readJson('task_graph.json');
const conceptMap = readJson('concept_map.json');
const requiredSyncs = readJson('required_syncs.json');

const taskConcept = new Map();
for (const entry of conceptMap.tasks || []) {
  if (entry && entry.task_id && entry.concept) {
    taskConcept.set(String(entry.task_id), String(entry.concept));
  }
}

const dependsOnByTask = new Map();
const conceptDepsByTask = new Map();
for (const edge of taskGraph.edges || []) {
  if (!edge || !edge.from || !edge.to) {
    continue;
  }
  const fromId = String(edge.from);
  const toId = String(edge.to);
  if (!dependsOnByTask.has(toId)) {
    dependsOnByTask.set(toId, new Set());
  }
  dependsOnByTask.get(toId).add(fromId);

  const fromConcept = taskConcept.get(fromId);
  const toConcept = taskConcept.get(toId);
  if (fromConcept && toConcept && fromConcept !== toConcept) {
    if (!conceptDepsByTask.has(toId)) {
      conceptDepsByTask.set(toId, new Set());
    }
    conceptDepsByTask.get(toId).add(fromConcept);
  }
}

const tasks = (taskGraph.tasks || []).map((task) => {
  const id = String(task.task_id ?? '');
  const concept = taskConcept.get(id) ?? null;
  const entry = {
    id,
    concept,
    type: task.type ?? null,
    priority: task.priority ?? null,
    timestamp: task.timestamp ?? null,
    depends_on: Array.from(dependsOnByTask.get(id) || []).sort(),
  };

  const conceptDeps = Array.from(conceptDepsByTask.get(id) || []).sort();
  if (conceptDeps.length) {
    entry.concept_dependencies = conceptDeps;
  }

  Object.keys(entry).forEach((key) => {
    if (entry[key] === null) {
      delete entry[key];
    }
  });

  return entry;
});

tasks.sort((a, b) => a.id.localeCompare(b.id));

const concepts = Array.from(
  new Set((conceptMap.tasks || []).map((entry) => entry?.concept).filter(Boolean).map(String))
).sort();

const syncs = (requiredSyncs.synchronizations || []).map((sync) => ({
  name: String(sync.sync_id),
  from: String(sync.from_concept),
  to: String(sync.to_concept),
}));

syncs.sort((a, b) => a.name.localeCompare(b.name));

const payload = {
  concepts,
  synchronizations: syncs,
  tasks,
};

fs.writeFileSync(outPath, JSON.stringify(payload, null, 2));
NODE
else
  INPUT="$ROOT/templates/arbitration/fixture.json"
  echo "No planner output directory detected; using fixture input." >&2
fi

if [[ ! -f "$INPUT" ]]; then
  echo "Arbitration input not found: $INPUT" >&2
  exit 1
fi

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
