#!/usr/bin/env node
'use strict';

const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const { spawnSync } = require('node:child_process');

const HOOK_POINTS = new Set([
  'pre_planning',
  'post_planning',
  'pre_arbitration',
  'post_arbitration',
  'observability_only',
]);

function usage() {
  console.error('Usage: node plugins/plugin-runner.js --hook <hook> --input <json> --role <role> --concept <concept> [--registry <path>] [--log <path>]');
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

function loadRegistry(registryPath) {
  const loader = path.join(__dirname, 'plugin-loader.js');
  const result = spawnSync('node', [loader, registryPath], { encoding: 'utf8' });
  if (result.status !== 0) {
    throw new Error(result.stderr || 'Failed to load plugin registry.');
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

function runPlugin(plugin, payload) {
  const entryPath = path.resolve(process.cwd(), plugin.entrypoint);
  if (!fs.existsSync(entryPath)) {
    return {
      status: 'failed',
      error: `Entrypoint not found: ${plugin.entrypoint}`,
    };
  }
  const result = spawnSync('node', [entryPath], {
    input: JSON.stringify(payload),
    encoding: 'utf8',
  });

  if (result.status !== 0) {
    return {
      status: 'failed',
      error: result.stderr || `Plugin '${plugin.name}' failed with status ${result.status}`,
    };
  }

  let output;
  try {
    output = JSON.parse(result.stdout || '{}');
  } catch (err) {
    return {
      status: 'failed',
      error: `Plugin '${plugin.name}' produced invalid JSON output.`,
    };
  }

  return { status: 'ok', output };
}

function main() {
  const args = process.argv.slice(2);
  let hook = null;
  let inputRaw = null;
  let role = null;
  let concept = null;
  let registryPath = path.join(process.cwd(), 'plugins', 'registry.yaml');
  let logPath = path.join(process.cwd(), 'logs', 'plugin-events.jsonl');

  for (let i = 0; i < args.length; i += 1) {
    const arg = args[i];
    if (arg === '--hook' && args[i + 1]) {
      hook = args[i + 1];
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

  if (!hook || !inputRaw || !role || !concept) {
    usage();
    process.exit(1);
  }

  if (!HOOK_POINTS.has(hook)) {
    console.error(`Unknown hook point: ${hook}`);
    process.exit(1);
  }

  if (typeof concept !== 'string' || concept.trim() === '') {
    console.error('Plugin invocation requires a non-empty concept.');
    process.exit(1);
  }
  concept = concept.trim();

  let input;
  try {
    input = readJsonInput(inputRaw);
  } catch (err) {
    console.error(err.message);
    process.exit(1);
  }

  const inputConcept = Object.prototype.hasOwnProperty.call(input, 'concept') ? input.concept : undefined;
  if (Array.isArray(inputConcept)) {
    console.error('Plugin input may not declare multiple concepts.');
    process.exit(1);
  }
  if (typeof inputConcept === 'string' && inputConcept && inputConcept !== concept) {
    console.error(`Plugin input concept '${inputConcept}' does not match invocation concept '${concept}'.`);
    process.exit(1);
  }

  const inputConcepts = Object.prototype.hasOwnProperty.call(input, 'concepts') ? input.concepts : undefined;
  if (Array.isArray(inputConcepts)) {
    const unique = new Set(inputConcepts.map((item) => String(item)));
    if (unique.size > 1 || (unique.size === 1 && !unique.has(concept))) {
      console.error('Plugin input may not span multiple concepts.');
      process.exit(1);
    }
  } else if (inputConcepts !== undefined) {
    console.error('Plugin input concepts must be an array when provided.');
    process.exit(1);
  }

  const conceptDependencies = normalizeStringList(
    input && (input.concept_dependencies || input.depends_on_concepts || input.concept_deps)
  );
  if (conceptDependencies.length) {
    console.error('Plugin input may not declare concept dependencies.');
    process.exit(1);
  }

  let registry;
  try {
    registry = loadRegistry(registryPath);
  } catch (err) {
    console.error(err.message);
    process.exit(1);
  }

  const plugins = (registry.plugins || []).filter((plugin) => plugin.enabled === true);
  const eligible = plugins.filter((plugin) => Array.isArray(plugin.hook_points) && plugin.hook_points.includes(hook));

  const payload = {
    hook,
    role,
    concept,
    input,
  };

  const inputDigest = crypto.createHash('sha256').update(stableStringify(payload)).digest('hex');

  fs.mkdirSync(path.dirname(logPath), { recursive: true });

  const results = [];

  for (const plugin of eligible) {
    if (Array.isArray(plugin.allowed_roles) && !plugin.allowed_roles.includes(role)) {
      results.push({ name: plugin.name, status: 'skipped', reason: 'role_not_allowed' });
      continue;
    }

    const entry = {
      timestamp: new Date().toISOString(),
      plugin: plugin.name,
      hook,
      role,
      concept,
      input_digest: inputDigest,
      entrypoint: plugin.entrypoint,
      status: 'started',
    };
    writeLog(entry, logPath);

    const result = runPlugin(plugin, payload);

    if (result.status !== 'ok') {
      const errorEntry = { ...entry, status: 'failed', error: result.error };
      writeLog(errorEntry, logPath);
      results.push({ name: plugin.name, status: 'failed', error: result.error });
      continue;
    }

    const outputDigest = crypto.createHash('sha256').update(stableStringify(result.output)).digest('hex');
    const successEntry = { ...entry, status: 'ok', output_digest: outputDigest };
    writeLog(successEntry, logPath);
    results.push({ name: plugin.name, status: 'ok', output: result.output });
  }

  process.stdout.write(`${JSON.stringify({ hook, results }, null, 2)}\n`);
}

main();
