#!/usr/bin/env node
'use strict';

const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');

const TYPE_ALIASES = {
  plan: 'planning',
  planning: 'planning',
  execute: 'execution',
  execution: 'execution',
  validate: 'validation',
  validation: 'validation',
};

const TYPE_ORDER = {
  planning: 3,
  validation: 2,
  execution: 1,
};

const PRIORITY_LABELS = {
  critical: 100,
  high: 75,
  medium: 50,
  low: 25,
  none: 0,
};

const INFERRED_PRIORITY = {
  planning: 50,
  validation: 40,
  execution: 30,
  unknown: 10,
};

function usage() {
  console.error('Usage: node arbitration/arbitrator.js --input <tasks.json> [--output <out.json>]');
  console.error('If --input is omitted, reads JSON from stdin.');
}

function readStdin() {
  return new Promise((resolve, reject) => {
    let data = '';
    process.stdin.setEncoding('utf8');
    process.stdin.on('data', (chunk) => {
      data += chunk;
    });
    process.stdin.on('end', () => resolve(data));
    process.stdin.on('error', reject);
  });
}

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

function digestInput(value) {
  const canonical = stableStringify(value);
  return crypto.createHash('sha256').update(canonical).digest('hex');
}

function normalizeList(value) {
  if (value === undefined || value === null) {
    return [];
  }
  if (Array.isArray(value)) {
    return value.filter((item) => item !== null && item !== undefined).map((item) => String(item));
  }
  return [String(value)];
}

function parsePriority(value, type) {
  if (value === undefined || value === null || value === '') {
    return { value: INFERRED_PRIORITY[type] ?? INFERRED_PRIORITY.unknown, inferred: true };
  }
  if (typeof value === 'number') {
    return { value, inferred: false };
  }
  const lowered = String(value).toLowerCase();
  if (PRIORITY_LABELS[lowered] !== undefined) {
    return { value: PRIORITY_LABELS[lowered], inferred: false };
  }
  const numeric = Number(value);
  if (!Number.isNaN(numeric)) {
    return { value: numeric, inferred: false };
  }
  return { value: INFERRED_PRIORITY[type] ?? INFERRED_PRIORITY.unknown, inferred: true };
}

function parseTimestamp(value) {
  if (value === undefined || value === null || value === '') {
    return { value: null, error: 'timestamp_missing' };
  }
  if (typeof value === 'number') {
    if (value < 1e12) {
      return { value: value * 1000, error: null };
    }
    return { value, error: null };
  }
  const parsed = Date.parse(String(value));
  if (Number.isNaN(parsed)) {
    return { value: null, error: 'timestamp_invalid' };
  }
  return { value: parsed, error: null };
}

function listConceptsFromDir(root) {
  const conceptsDir = path.join(root, 'concepts');
  if (!fs.existsSync(conceptsDir)) {
    return [];
  }
  return fs
    .readdirSync(conceptsDir, { withFileTypes: true })
    .filter((entry) => entry.isDirectory())
    .map((entry) => entry.name)
    .filter((name) => !name.startsWith('.'))
    .sort();
}

function parseSyncFile(filePath) {
  const content = fs.readFileSync(filePath, 'utf8');
  const lines = content.split(/\r?\n/);
  const data = {
    name: null,
    from: null,
    to: null,
    direction: null,
    bidirectional: false,
    concepts: [],
    allowCycle: false,
  };
  let inConceptList = false;
  for (const rawLine of lines) {
    const line = rawLine.replace(/\s+#.*$/, '').trim();
    if (!line) {
      continue;
    }
    if (line.startsWith('- ')) {
      if (inConceptList) {
        data.concepts.push(line.slice(2).trim());
      }
      continue;
    }
    if (line.includes(':')) {
      const idx = line.indexOf(':');
      const key = line.slice(0, idx).trim();
      const value = line.slice(idx + 1).trim();
      inConceptList = false;
      if (key === 'concepts') {
        if (value.startsWith('[') && value.endsWith(']')) {
          const inner = value.slice(1, -1).trim();
          data.concepts = inner ? inner.split(',').map((item) => item.trim().replace(/^['"]|['"]$/g, '')) : [];
        } else if (!value) {
          inConceptList = true;
        } else {
          data.concepts = [value.replace(/^['"]|['"]$/g, '')];
        }
        continue;
      }
      if (key === 'name') {
        data.name = value.replace(/^['"]|['"]$/g, '');
      } else if (key === 'from') {
        data.from = value.replace(/^['"]|['"]$/g, '');
      } else if (key === 'to') {
        data.to = value.replace(/^['"]|['"]$/g, '');
      } else if (key === 'direction') {
        data.direction = value.replace(/^['"]|['"]$/g, '').toLowerCase();
      } else if (key === 'bidirectional') {
        data.bidirectional = ['true', 'yes', '1'].includes(value.toLowerCase());
      } else if (key === 'allow_cycle' || key === 'allowCycle') {
        data.allowCycle = ['true', 'yes', '1'].includes(value.toLowerCase());
      }
    }
  }

  if (!data.name) {
    data.name = path.basename(filePath, path.extname(filePath));
  }
  if (!data.from || !data.to) {
    if (data.concepts.length === 2 && (data.bidirectional || data.direction === 'bidirectional' || data.direction === 'both')) {
      data.from = data.concepts[0];
      data.to = data.concepts[1];
      data.bidirectional = true;
    }
  }
  return data;
}

function listSynchronizationsFromDir(root) {
  const syncDir = path.join(root, 'synchronizations');
  if (!fs.existsSync(syncDir)) {
    return [];
  }
  const files = fs
    .readdirSync(syncDir, { withFileTypes: true })
    .filter((entry) => entry.isFile() && /\.ya?ml$/i.test(entry.name))
    .map((entry) => path.join(syncDir, entry.name))
    .sort();
  return files.map((filePath) => ({ ...parseSyncFile(filePath), filePath }));
}

function buildSyncIndex(syncs) {
  const map = new Map();
  const pairs = new Set();
  for (const sync of syncs) {
    if (!sync.name) {
      continue;
    }
    map.set(sync.name, sync);
    if (sync.from && sync.to) {
      const key = [sync.from, sync.to].sort().join('::');
      pairs.add(key);
      if (sync.bidirectional || sync.direction === 'bidirectional' || sync.direction === 'both') {
        pairs.add([sync.to, sync.from].sort().join('::'));
      }
    }
  }
  return { map, pairs };
}

function normalizeTask(task, index) {
  const id = task.id ?? task.task_id ?? task.taskId ?? `task-${index + 1}`;
  const concept = task.concept ?? task.concept_owner ?? task.owner_concept ?? task.concept_id;
  const typeRaw = task.type ?? task.task_type ?? task.kind;
  const type = TYPE_ALIASES[String(typeRaw || '').toLowerCase()] ?? null;
  const priorityInfo = parsePriority(task.priority ?? task.priority_hint, type ?? 'unknown');
  const timestampInfo = parseTimestamp(task.timestamp ?? task.created_at ?? task.time);

  const syncDependencies = normalizeList(task.sync_dependencies ?? task.synchronizations ?? task.syncs ?? task.sync);
  const conceptDependencies = normalizeList(task.concept_dependencies ?? task.depends_on_concepts ?? task.concept_deps);
  const dependsOnTasks = normalizeList(task.depends_on ?? task.blocked_by ?? task.dependsOn);

  return {
    raw: task,
    id: String(id),
    concept: concept ? String(concept) : null,
    type,
    priority: priorityInfo.value,
    priorityInferred: priorityInfo.inferred,
    timestamp: timestampInfo.value,
    timestampError: timestampInfo.error,
    syncDependencies,
    conceptDependencies,
    dependsOnTasks,
  };
}

function main() {
  const args = process.argv.slice(2);
  let inputPath = null;
  let outputPath = null;

  for (let i = 0; i < args.length; i += 1) {
    const arg = args[i];
    if (arg === '--input' && args[i + 1]) {
      inputPath = args[i + 1];
      i += 1;
    } else if (arg === '--output' && args[i + 1]) {
      outputPath = args[i + 1];
      i += 1;
    } else if (arg === '--help' || arg === '-h') {
      usage();
      process.exit(0);
    }
  }

  const run = async () => {
    let inputText = '';
    if (inputPath) {
      inputText = fs.readFileSync(inputPath, 'utf8');
    } else {
      inputText = await readStdin();
      if (!inputText.trim()) {
        usage();
        process.exit(1);
      }
    }

    let input;
    try {
      input = JSON.parse(inputText);
    } catch (err) {
      console.error(`Failed to parse JSON input: ${err.message}`);
      process.exit(1);
    }

    const tasksRaw = Array.isArray(input.tasks) ? input.tasks : [];
    const concepts = Array.isArray(input.concepts)
      ? input.concepts.map((value) => String(value)).sort()
      : listConceptsFromDir(process.cwd());
    const syncs = Array.isArray(input.synchronizations)
      ? input.synchronizations
      : listSynchronizationsFromDir(process.cwd());

    const syncIndex = buildSyncIndex(syncs);
    const conceptSet = new Set(concepts);

    const decisionLog = {
      generated_at: new Date().toISOString(),
      input_digest: digestInput(input),
      rules_version: '1.0',
      source: {
        concepts: input.concepts ? 'input' : concepts.length ? 'directory' : 'none',
        synchronizations: input.synchronizations ? 'input' : syncs.length ? 'directory' : 'none',
      },
      rules: [
        'normalize',
        'validate_required_fields',
        'validate_concepts',
        'validate_synchronizations',
        'validate_dependencies',
        'deterministic_sort',
        'concept_serialization',
      ],
      trace: [],
    };

    const normalized = tasksRaw.map((task, index) => normalizeTask(task, index));
    normalized.sort((a, b) => a.id.localeCompare(b.id));

    const rejected = [];
    const accepted = [];
    const allTaskIds = new Set(normalized.map((task) => task.id));

    for (const task of normalized) {
      const reasons = [];
      if (!task.id) {
        reasons.push('missing_id');
      }
      if (!task.concept) {
        reasons.push('missing_concept');
      }
      if (!task.type || !TYPE_ORDER[task.type]) {
        reasons.push('invalid_type');
      }
      if (task.timestampError) {
        reasons.push(task.timestampError);
      }

      if (concepts.length && task.concept && !conceptSet.has(task.concept)) {
        reasons.push('unknown_concept');
      }

      if (syncs.length && task.syncDependencies.length) {
        for (const syncName of task.syncDependencies) {
          const sync = syncIndex.map.get(syncName);
          if (!sync) {
            reasons.push(`unknown_sync:${syncName}`);
            continue;
          }
          if (task.concept && sync.from && sync.to) {
            const matches = sync.from === task.concept || sync.to === task.concept;
            if (!matches) {
              reasons.push(`sync_not_linked:${syncName}`);
            }
          }
        }
      }

      if (syncs.length && task.conceptDependencies.length && task.concept) {
        for (const dep of task.conceptDependencies) {
          if (concepts.length && !conceptSet.has(dep)) {
            reasons.push(`unknown_concept_dependency:${dep}`);
            continue;
          }
          const key = [task.concept, dep].sort().join('::');
          if (!syncIndex.pairs.has(key)) {
            reasons.push(`missing_sync_for_dependency:${dep}`);
          }
        }
      }

      if (task.dependsOnTasks.length) {
        for (const depTask of task.dependsOnTasks) {
          if (!allTaskIds.has(depTask)) {
            reasons.push(`unknown_task_dependency:${depTask}`);
          }
        }
      }

      if (reasons.length) {
        rejected.push({ task_id: task.id, reasons });
        decisionLog.trace.push({ task_id: task.id, rule: 'reject', reasons });
      } else {
        accepted.push(task);
        decisionLog.trace.push({
          task_id: task.id,
          rule: 'accept',
          priority: task.priority,
          priority_inferred: task.priorityInferred,
        });
      }
    }

    accepted.sort((a, b) => {
      if (b.priority !== a.priority) {
        return b.priority - a.priority;
      }
      if (TYPE_ORDER[b.type] !== TYPE_ORDER[a.type]) {
        return TYPE_ORDER[b.type] - TYPE_ORDER[a.type];
      }
      if (a.timestamp !== b.timestamp) {
        return a.timestamp - b.timestamp;
      }
      if (a.concept !== b.concept) {
        return a.concept.localeCompare(b.concept);
      }
      return a.id.localeCompare(b.id);
    });

    const ordered = [];
    const lastByConcept = new Map();
    for (const task of accepted) {
      if (task.concept && lastByConcept.has(task.concept)) {
        decisionLog.trace.push({
          task_id: task.id,
          rule: 'concept_serialization',
          serialized_after: lastByConcept.get(task.concept),
        });
      }
      ordered.push(task.id);
      if (task.concept) {
        lastByConcept.set(task.concept, task.id);
      }
    }

    const output = {
      status: rejected.length ? 'blocked' : 'ok',
      order: ordered,
      accepted: accepted.map((task) => ({
        task_id: task.id,
        concept: task.concept,
        type: task.type,
        priority: task.priority,
        timestamp: task.timestamp,
      })),
      blocked: rejected.sort((a, b) => a.task_id.localeCompare(b.task_id)),
      decision_log: decisionLog,
    };

    const outputText = JSON.stringify(output, null, 2);
    if (outputPath) {
      fs.writeFileSync(outputPath, outputText);
    } else {
      process.stdout.write(`${outputText}\n`);
    }
  };

  run().catch((err) => {
    console.error(err);
    process.exit(1);
  });
}

main();
