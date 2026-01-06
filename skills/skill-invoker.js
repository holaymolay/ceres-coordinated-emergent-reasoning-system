#!/usr/bin/env node
'use strict';

const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const { spawnSync } = require('node:child_process');

function usage() {
  console.error('Usage: node skills/skill-invoker.js --skill <name> --input <json> --role <role> --concept <concept> [--registry <path>] [--log <path>]');
}

function readJsonInput(value) {
  try {
    return JSON.parse(value);
  } catch (err) {
    throw new Error(`Invalid input JSON: ${err.message}`);
  }
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

function normalizeStringList(value) {
  if (value === undefined || value === null) {
    return [];
  }
  if (Array.isArray(value)) {
    return value.filter((item) => item !== null && item !== undefined).map((item) => String(item));
  }
  return [String(value)];
}

function normalizeSyncDependencies(value) {
  if (value === undefined || value === null) {
    return [];
  }
  const list = [];
  const add = (item) => {
    if (item === undefined || item === null) {
      return;
    }
    if (typeof item === 'string') {
      list.push(item);
      return;
    }
    if (item && typeof item === 'object') {
      if (typeof item.sync_id === 'string') {
        list.push(item.sync_id);
        return;
      }
      if (typeof item.name === 'string') {
        list.push(item.name);
      }
    }
  };
  if (Array.isArray(value)) {
    value.forEach(add);
  } else {
    add(value);
  }
  return list;
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
  };
  let inConceptList = false;
  for (const rawLine of lines) {
    const line = rawLine.replace(/\s+#.*$/, '').trim();
    if (!line) {
      continue;
    }
    if (line.startsWith('- ')) {
      if (inConceptList) {
        data.concepts.push(line.slice(2).trim().replace(/^['"]|['"]$/g, ''));
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
          data.concepts = inner
            ? inner.split(',').map((item) => item.trim().replace(/^['"]|['"]$/g, ''))
            : [];
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
      }
    }
  }

  if (!data.name) {
    data.name = path.basename(filePath, path.extname(filePath));
  }
  if ((!data.from || !data.to) && data.concepts.length === 2) {
    if (data.bidirectional || data.direction === 'bidirectional' || data.direction === 'both') {
      data.from = data.concepts[0];
      data.to = data.concepts[1];
      data.bidirectional = true;
    }
  }
  return data;
}

function loadSynchronizations(syncDir) {
  if (!fs.existsSync(syncDir)) {
    return new Map();
  }
  const entries = fs
    .readdirSync(syncDir, { withFileTypes: true })
    .filter((entry) => entry.isFile() && /\.ya?ml$/i.test(entry.name))
    .map((entry) => path.join(syncDir, entry.name));
  const map = new Map();
  for (const filePath of entries) {
    const sync = parseSyncFile(filePath);
    if (sync.name) {
      map.set(sync.name, sync);
    }
  }
  return map;
}

function syncIncludesConcept(sync, concept) {
  if (!sync || !concept) {
    return false;
  }
  if (sync.from === concept || sync.to === concept) {
    return true;
  }
  if (Array.isArray(sync.concepts) && sync.concepts.includes(concept)) {
    return true;
  }
  return false;
}


function loadRegistry(registryPath) {
  const loader = path.join(__dirname, 'skill-loader.js');
  const result = spawnSync('node', [loader, registryPath], { encoding: 'utf8' });
  if (result.status !== 0) {
    throw new Error(result.stderr || 'Failed to load skill registry.');
  }
  return JSON.parse(result.stdout);
}

function writeLog(entry, logPath) {
  if (!logPath) {
    return;
  }
  const line = JSON.stringify(entry);
  fs.appendFileSync(logPath, `${line}\n`);
}

function main() {
  const args = process.argv.slice(2);
  let skillName = null;
  let inputRaw = null;
  let role = null;
  let concept = null;
  let registryPath = path.join(process.cwd(), 'skills', 'registry.yaml');
  let logPath = path.join(process.cwd(), 'logs', 'skill-invocations.jsonl');

  for (let i = 0; i < args.length; i += 1) {
    const arg = args[i];
    if (arg === '--skill' && args[i + 1]) {
      skillName = args[i + 1];
      i += 1;
    } else if (arg === '--input' && args[i + 1]) {
      inputRaw = args[i + 1];
      i += 1;
    } else if (arg === '--role' && args[i + 1]) {
      role = args[i + 1];
      i += 1;
    } else if (arg === '--concept' && args[i + 1]) {
      concept = args[i + 1];
      i += 1;
    } else if (arg === '--registry' && args[i + 1]) {
      registryPath = path.resolve(args[i + 1]);
      i += 1;
    } else if (arg === '--log' && args[i + 1]) {
      logPath = path.resolve(args[i + 1]);
      i += 1;
    } else if (arg === '--help' || arg === '-h') {
      usage();
      process.exit(0);
    }
  }

  if (!skillName || !inputRaw || !role || !concept) {
    usage();
    process.exit(1);
  }

  let input;
  try {
    input = readJsonInput(inputRaw);
  } catch (err) {
    console.error(err.message);
    process.exit(1);
  }

  let registry;
  try {
    registry = loadRegistry(registryPath);
  } catch (err) {
    console.error(err.message);
    process.exit(1);
  }

  const skill = (registry.skills || []).find((item) => item.name === skillName);
  if (!skill) {
    console.error(`Skill not found: ${skillName}`);
    process.exit(1);
  }

  if (!Array.isArray(skill.allowed_roles) || !skill.allowed_roles.includes(role)) {
    console.error(`Role '${role}' is not authorized for skill '${skillName}'.`);
    process.exit(1);
  }

  if (skill.concept_scope && skill.concept_scope !== '*' && skill.concept_scope !== concept) {
    console.error(`Skill '${skillName}' is scoped to concept '${skill.concept_scope}', not '${concept}'.`);
    process.exit(1);
  }

  if (typeof concept !== 'string' || concept.trim() === '') {
    console.error('Skill invocation requires a non-empty concept.');
    process.exit(1);
  }
  concept = concept.trim();

  const inputConcept = input && Object.prototype.hasOwnProperty.call(input, 'concept') ? input.concept : undefined;
  if (Array.isArray(inputConcept)) {
    console.error('Skill input may not declare multiple concepts.');
    process.exit(1);
  }
  if (typeof inputConcept === 'string' && inputConcept && inputConcept !== concept) {
    console.error(`Skill input concept '${inputConcept}' does not match invocation concept '${concept}'.`);
    process.exit(1);
  }

  const inputConcepts = input && Object.prototype.hasOwnProperty.call(input, 'concepts') ? input.concepts : undefined;
  if (Array.isArray(inputConcepts)) {
    const unique = new Set(inputConcepts.map((item) => String(item)));
    if (unique.size > 1 || (unique.size === 1 && !unique.has(concept))) {
      console.error('Skill input may not span multiple concepts.');
      process.exit(1);
    }
  } else if (inputConcepts !== undefined) {
    console.error('Skill input concepts must be an array when provided.');
    process.exit(1);
  }

  const conceptDependencies = normalizeStringList(
    input && (input.concept_dependencies || input.depends_on_concepts || input.concept_deps)
  );
  if (conceptDependencies.length) {
    console.error('Skill input may not declare concept dependencies.');
    process.exit(1);
  }

  const syncDependencies = normalizeSyncDependencies(
    input && (input.sync_dependencies || input.synchronizations || input.syncs || input.sync)
  );
  if (syncDependencies.length) {
    const syncDir = path.join(process.cwd(), 'synchronizations');
    if (!fs.existsSync(syncDir)) {
      console.error('Synchronizations directory not found; cannot validate sync dependencies.');
      process.exit(1);
    }
    const syncIndex = loadSynchronizations(syncDir);
    for (const syncName of syncDependencies) {
      const sync = syncIndex.get(syncName);
      if (!sync) {
        console.error(`Unknown synchronization '${syncName}'.`);
        process.exit(1);
      }
      if (!syncIncludesConcept(sync, concept)) {
        console.error(`Synchronization '${syncName}' does not include concept '${concept}'.`);
        process.exit(1);
      }
    }
  }

  const entryPath = path.resolve(process.cwd(), skill.entrypoint);
  if (!fs.existsSync(entryPath)) {
    console.error(`Skill entrypoint not found: ${skill.entrypoint}`);
    process.exit(1);
  }

  const payload = {
    skill: skill.name,
    role,
    concept,
    input,
  };

  const inputDigest = crypto.createHash('sha256').update(stableStringify(payload)).digest('hex');
  const logEntry = {
    timestamp: new Date().toISOString(),
    skill: skill.name,
    role,
    concept,
    input_digest: inputDigest,
    entrypoint: skill.entrypoint,
    status: 'started',
  };

  if (syncDependencies.length) {
    logEntry.sync_dependencies = syncDependencies;
  }

  fs.mkdirSync(path.dirname(logPath), { recursive: true });
  writeLog(logEntry, logPath);

  const result = spawnSync('node', [entryPath], {
    input: JSON.stringify(payload),
    encoding: 'utf8',
  });

  if (result.status !== 0) {
    const errorEntry = {
      ...logEntry,
      status: 'failed',
      error: result.stderr || `Skill '${skill.name}' failed with status ${result.status}`,
    };
    writeLog(errorEntry, logPath);
    console.error(errorEntry.error);
    process.exit(1);
  }

  let output;
  try {
    output = JSON.parse(result.stdout || '{}');
  } catch (err) {
    const parseError = `Skill '${skill.name}' produced invalid JSON output.`;
    const errorEntry = { ...logEntry, status: 'failed', error: parseError };
    writeLog(errorEntry, logPath);
    console.error(parseError);
    process.exit(1);
  }

  const successEntry = { ...logEntry, status: 'ok', output_digest: crypto.createHash('sha256').update(stableStringify(output)).digest('hex') };
  writeLog(successEntry, logPath);

  process.stdout.write(`${JSON.stringify(output, null, 2)}\n`);
}

main();
