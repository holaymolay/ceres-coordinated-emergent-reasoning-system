#!/usr/bin/env node
'use strict';

const fs = require('node:fs');
const path = require('node:path');

function stripComment(line) {
  let inSingle = false;
  let inDouble = false;
  for (let i = 0; i < line.length; i += 1) {
    const ch = line[i];
    if (ch === '"' && !inSingle) {
      inDouble = !inDouble;
    } else if (ch === "'" && !inDouble) {
      inSingle = !inSingle;
    } else if (ch === '#' && !inSingle && !inDouble) {
      return line.slice(0, i);
    }
  }
  return line;
}

function splitKeyValue(line) {
  const idx = line.indexOf(':');
  if (idx === -1) {
    throw new Error(`Invalid YAML line (missing ':'): ${line}`);
  }
  const key = line.slice(0, idx).trim();
  const rest = line.slice(idx + 1).trim();
  return { key, rest };
}

function splitInlineList(value) {
  const items = [];
  let current = '';
  let inSingle = false;
  let inDouble = false;
  for (let i = 0; i < value.length; i += 1) {
    const ch = value[i];
    if (ch === '"' && !inSingle) {
      inDouble = !inDouble;
      current += ch;
      continue;
    }
    if (ch === "'" && !inDouble) {
      inSingle = !inSingle;
      current += ch;
      continue;
    }
    if (ch === ',' && !inSingle && !inDouble) {
      items.push(current.trim());
      current = '';
      continue;
    }
    current += ch;
  }
  if (current.trim() !== '') {
    items.push(current.trim());
  }
  return items;
}

function parseScalar(value) {
  if (value === '') {
    return '';
  }
  if ((value.startsWith('"') && value.endsWith('"')) || (value.startsWith("'") && value.endsWith("'"))) {
    return value.slice(1, -1);
  }
  if (value === 'true') {
    return true;
  }
  if (value === 'false') {
    return false;
  }
  if (value === 'null') {
    return null;
  }
  if (/^-?\d+(\.\d+)?$/.test(value)) {
    return Number(value);
  }
  if (value.startsWith('[') && value.endsWith(']')) {
    const inner = value.slice(1, -1).trim();
    if (inner === '') {
      return [];
    }
    return splitInlineList(inner).map((item) => parseScalar(item));
  }
  return value;
}

function nextNonEmptyLine(lines, start) {
  for (let i = start; i < lines.length; i += 1) {
    if (lines[i].text.trim() !== '') {
      return lines[i];
    }
  }
  return null;
}

function parseBlock(lines, startIndex, baseIndent) {
  const obj = {};
  let arr = null;
  let i = startIndex;

  while (i < lines.length) {
    const entry = lines[i];
    if (entry.text.trim() === '') {
      i += 1;
      continue;
    }
    const indent = entry.indent;
    if (indent < baseIndent) {
      break;
    }

    const trimmed = entry.text.trim();
    if (trimmed.startsWith('- ')) {
      if (indent > baseIndent) {
        break;
      }
      if (!arr) {
        arr = [];
      }
      const itemText = trimmed.slice(2).trim();
      if (itemText === '') {
        const nextLine = nextNonEmptyLine(lines, i + 1);
        if (!nextLine || nextLine.indent <= indent) {
          arr.push({});
          i += 1;
          continue;
        }
        const [child, nextIndex] = parseBlock(lines, i + 1, nextLine.indent);
        arr.push(child);
        i = nextIndex;
        continue;
      }
      if (itemText.includes(':')) {
        const { key, rest } = splitKeyValue(itemText);
        if (rest === '') {
          const nextLine = nextNonEmptyLine(lines, i + 1);
          if (!nextLine || nextLine.indent <= indent) {
            arr.push({ [key]: {} });
            i += 1;
            continue;
          }
          const [child, nextIndex] = parseBlock(lines, i + 1, nextLine.indent);
          arr.push({ [key]: child });
          i = nextIndex;
          continue;
        }
        arr.push({ [key]: parseScalar(rest) });
        i += 1;
        continue;
      }
      arr.push(parseScalar(itemText));
      i += 1;
      continue;
    }

    if (arr) {
      break;
    }
    if (indent > baseIndent) {
      break;
    }
    const { key, rest } = splitKeyValue(trimmed);
    if (rest === '') {
      const nextLine = nextNonEmptyLine(lines, i + 1);
      if (!nextLine || nextLine.indent <= indent) {
        obj[key] = {};
        i += 1;
        continue;
      }
      const [child, nextIndex] = parseBlock(lines, i + 1, nextLine.indent);
      obj[key] = child;
      i = nextIndex;
      continue;
    }
    obj[key] = parseScalar(rest);
    i += 1;
  }

  return [arr ?? obj, i];
}

function parseSimpleYaml(text, filePath) {
  const rawLines = text.split(/\r?\n/);
  const lines = rawLines.map((line) => {
    const withoutTabs = line.replace(/\t/g, '  ');
    const withoutComments = stripComment(withoutTabs);
    const trimmedRight = withoutComments.replace(/\s+$/, '');
    const trimmed = trimmedRight.trim();
    if (trimmed === '---' || trimmed === '...') {
      return { indent: 0, text: '' };
    }
    const indent = trimmedRight.match(/^\s*/)[0].length;
    return { indent, text: trimmedRight };
  });

  try {
    const [value] = parseBlock(lines, 0, 0);
    return value;
  } catch (err) {
    throw new Error(`YAML parse error in ${filePath}: ${err.message}`);
  }
}

function extractStringList(value) {
  const result = [];
  const push = (item) => {
    if (typeof item === 'string' && item.trim() !== '') {
      result.push(item.trim());
    }
  };

  if (Array.isArray(value)) {
    for (const item of value) {
      if (typeof item === 'string') {
        push(item);
      } else if (item && typeof item === 'object') {
        if (typeof item.name === 'string') {
          push(item.name);
        } else if (typeof item.id === 'string') {
          push(item.id);
        }
      }
    }
  } else if (typeof value === 'string') {
    push(value);
  } else if (value && typeof value === 'object') {
    if (typeof value.name === 'string') {
      push(value.name);
    } else if (typeof value.id === 'string') {
      push(value.id);
    }
  }

  return result;
}

function normalizeManifest(manifest) {
  const deps = manifest.dependencies;
  let read = [];
  let write = [];
  if (deps !== undefined) {
    if (Array.isArray(deps) || typeof deps === 'string') {
      read = extractStringList(deps);
    } else if (deps && typeof deps === 'object') {
      read = extractStringList(deps.read ?? deps.in ?? deps.input);
      write = extractStringList(deps.write ?? deps.out ?? deps.output);
    }
  }

  const syncs = manifest.synchronizations ?? manifest.syncs;
  let outgoing = [];
  let incoming = [];
  if (syncs !== undefined) {
    if (Array.isArray(syncs) || typeof syncs === 'string') {
      outgoing = extractStringList(syncs);
    } else if (syncs && typeof syncs === 'object') {
      outgoing = extractStringList(syncs.outgoing ?? syncs.out);
      incoming = extractStringList(syncs.incoming ?? syncs.in);
    }
  }

  return { dependencies: { read, write }, synchronizations: { outgoing, incoming } };
}

function isBidirectional(value) {
  if (typeof value !== 'string') {
    return false;
  }
  const normalized = value.toLowerCase();
  return ['bidirectional', 'both', 'two-way', 'two_way', 'two way'].includes(normalized);
}

function normalizeSynchronization(sync, filePath) {
  const name =
    sync.name ||
    sync.id ||
    sync.synchronization ||
    sync.sync ||
    path.basename(filePath, path.extname(filePath));

  const allowCycle = Boolean(
    sync.allow_cycle ||
      sync.allowCycle ||
      sync.allow_cycles ||
      sync.allowCycles ||
      sync.cycle_allowed ||
      sync.cycleAllowed
  );

  const from = sync.from ?? sync.source ?? sync.origin;
  const to = sync.to ?? sync.target ?? sync.destination;
  const direction = sync.direction;
  const concepts = extractStringList(sync.concepts ?? sync.nodes ?? sync.participants);

  let bidirectional = false;
  let resolvedFrom = from;
  let resolvedTo = to;

  if (!resolvedFrom || !resolvedTo) {
    if (concepts.length === 2 && isBidirectional(direction)) {
      resolvedFrom = concepts[0];
      resolvedTo = concepts[1];
      bidirectional = true;
    }
  }

  return {
    name,
    from: resolvedFrom,
    to: resolvedTo,
    bidirectional,
    allowCycle,
    filePath,
  };
}

function listYamlFiles(dirPath) {
  if (!fs.existsSync(dirPath)) {
    return [];
  }
  return fs
    .readdirSync(dirPath, { withFileTypes: true })
    .filter((entry) => entry.isFile() && /\.ya?ml$/i.test(entry.name))
    .map((entry) => path.join(dirPath, entry.name));
}

function loadYaml(filePath) {
  const content = fs.readFileSync(filePath, 'utf8');
  return parseSimpleYaml(content, filePath);
}

function buildAdjacency(concepts, edges) {
  const adjacency = new Map();
  for (const name of concepts) {
    adjacency.set(name, []);
  }
  for (const edge of edges) {
    if (!adjacency.has(edge.from)) {
      adjacency.set(edge.from, []);
    }
    adjacency.get(edge.from).push(edge);
  }
  for (const edgesList of adjacency.values()) {
    edgesList.sort((a, b) => `${a.to}:${a.syncName}`.localeCompare(`${b.to}:${b.syncName}`));
  }
  return adjacency;
}

function findSccs(nodes, adjacency) {
  const indexMap = new Map();
  const lowlink = new Map();
  const onStack = new Set();
  const stack = [];
  const sccs = [];
  let index = 0;

  function strongconnect(node) {
    indexMap.set(node, index);
    lowlink.set(node, index);
    index += 1;
    stack.push(node);
    onStack.add(node);

    for (const edge of adjacency.get(node) || []) {
      const next = edge.to;
      if (!indexMap.has(next)) {
        strongconnect(next);
        lowlink.set(node, Math.min(lowlink.get(node), lowlink.get(next)));
      } else if (onStack.has(next)) {
        lowlink.set(node, Math.min(lowlink.get(node), indexMap.get(next)));
      }
    }

    if (lowlink.get(node) === indexMap.get(node)) {
      const component = [];
      let w = null;
      do {
        w = stack.pop();
        onStack.delete(w);
        component.push(w);
      } while (w !== node);
      sccs.push(component);
    }
  }

  for (const node of nodes) {
    if (!indexMap.has(node)) {
      strongconnect(node);
    }
  }

  return sccs;
}

function main() {
  const args = process.argv.slice(2);
  let root = process.cwd();
  for (let i = 0; i < args.length; i += 1) {
    if (args[i] === '--root' && args[i + 1]) {
      root = path.resolve(args[i + 1]);
      i += 1;
    }
  }

  const conceptsDir = path.join(root, 'concepts');
  const syncDir = path.join(root, 'synchronizations');

  if (!fs.existsSync(conceptsDir)) {
    console.log(`No concepts directory found at ${conceptsDir}; skipping validation.`);
    return;
  }

  const conceptEntries = fs
    .readdirSync(conceptsDir, { withFileTypes: true })
    .filter((entry) => entry.isDirectory())
    .map((entry) => entry.name)
    .filter((name) => !name.startsWith('.'))
    .sort();

  const errors = [];
  const concepts = new Map();

  for (const conceptName of conceptEntries) {
    const manifestPath = path.join(conceptsDir, conceptName, 'manifest.yaml');
    if (!fs.existsSync(manifestPath)) {
      errors.push(`Concept '${conceptName}' is missing manifest.yaml at ${manifestPath}.`);
      continue;
    }
    let manifest;
    try {
      manifest = loadYaml(manifestPath);
    } catch (err) {
      errors.push(err.message);
      continue;
    }
    const normalized = normalizeManifest(manifest || {});
    concepts.set(conceptName, {
      name: conceptName,
      manifestPath,
      dependencies: normalized.dependencies,
      synchronizations: normalized.synchronizations,
    });
  }

  const syncFiles = listYamlFiles(syncDir).sort();
  const syncs = new Map();
  for (const syncPath of syncFiles) {
    let sync;
    try {
      sync = loadYaml(syncPath);
    } catch (err) {
      errors.push(err.message);
      continue;
    }
    const normalized = normalizeSynchronization(sync || {}, syncPath);
    if (!normalized.from || !normalized.to) {
      errors.push(`Synchronization '${normalized.name}' missing 'from'/'to' concepts. File: ${syncPath}.`);
      continue;
    }
    syncs.set(normalized.name, normalized);
  }

  for (const [conceptName, concept] of concepts.entries()) {
    for (const syncName of concept.synchronizations.outgoing) {
      if (!syncs.has(syncName)) {
        errors.push(
          `Concept '${conceptName}' declares outgoing synchronization '${syncName}' but no file exists in ${syncDir}. Manifest: ${concept.manifestPath}.`
        );
      }
    }
    for (const syncName of concept.synchronizations.incoming) {
      if (!syncs.has(syncName)) {
        errors.push(
          `Concept '${conceptName}' declares incoming synchronization '${syncName}' but no file exists in ${syncDir}. Manifest: ${concept.manifestPath}.`
        );
      }
    }
  }

  const edges = [];
  for (const sync of syncs.values()) {
    if (!concepts.has(sync.from)) {
      errors.push(
        `Synchronization '${sync.name}' references unknown Concept '${sync.from}'. File: ${sync.filePath}.`
      );
    }
    if (!concepts.has(sync.to)) {
      errors.push(`Synchronization '${sync.name}' references unknown Concept '${sync.to}'. File: ${sync.filePath}.`);
    }

    edges.push({
      from: sync.from,
      to: sync.to,
      syncName: sync.name,
      allowCycle: sync.allowCycle,
      filePath: sync.filePath,
    });

    if (sync.bidirectional) {
      edges.push({
        from: sync.to,
        to: sync.from,
        syncName: sync.name,
        allowCycle: sync.allowCycle,
        filePath: sync.filePath,
      });
    }

    const fromConcept = concepts.get(sync.from);
    const toConcept = concepts.get(sync.to);
    if (fromConcept && !fromConcept.synchronizations.outgoing.includes(sync.name)) {
      errors.push(
        `Synchronization '${sync.name}' is not listed as outgoing for Concept '${sync.from}'. Manifest: ${fromConcept.manifestPath}.`
      );
    }
    if (toConcept && !toConcept.synchronizations.incoming.includes(sync.name)) {
      errors.push(
        `Synchronization '${sync.name}' is not listed as incoming for Concept '${sync.to}'. Manifest: ${toConcept.manifestPath}.`
      );
    }
  }

  const edgePairs = new Set();
  for (const edge of edges) {
    if (edge.from && edge.to) {
      const key = [edge.from, edge.to].sort().join('::');
      edgePairs.add(key);
    }
  }

  for (const [conceptName, concept] of concepts.entries()) {
    const allDeps = [
      ...concept.dependencies.read.map((dep) => ({ dep, mode: 'read' })),
      ...concept.dependencies.write.map((dep) => ({ dep, mode: 'write' })),
    ];
    for (const { dep, mode } of allDeps) {
      if (!concepts.has(dep)) {
        errors.push(
          `Concept '${conceptName}' declares ${mode} dependency on unknown Concept '${dep}'. Manifest: ${concept.manifestPath}.`
        );
        continue;
      }
      const key = [conceptName, dep].sort().join('::');
      if (!edgePairs.has(key)) {
        errors.push(
          `Concept '${conceptName}' declares ${mode} dependency on '${dep}' without an explicit synchronization. Manifest: ${concept.manifestPath}.`
        );
      }
    }
  }

  const adjacency = buildAdjacency([...concepts.keys()].sort(), edges);
  const sccs = findSccs([...concepts.keys()].sort(), adjacency);
  for (const scc of sccs) {
    const unique = scc.slice().sort();
    if (unique.length === 1) {
      const node = unique[0];
      const selfEdges = (adjacency.get(node) || []).filter((edge) => edge.to === node);
      if (selfEdges.length > 0 && selfEdges.some((edge) => !edge.allowCycle)) {
        const offenders = selfEdges
          .filter((edge) => !edge.allowCycle)
          .map((edge) => `${edge.syncName} (${edge.filePath})`)
          .sort();
        errors.push(
          `Cycle detected: '${node}' has a self-dependency without allow_cycle. Offending synchronizations: ${offenders.join(', ')}.`
        );
      }
      continue;
    }

    const edgesInScc = [];
    for (const node of unique) {
      for (const edge of adjacency.get(node) || []) {
        if (unique.includes(edge.to)) {
          edgesInScc.push(edge);
        }
      }
    }

    if (edgesInScc.length > 0) {
      const disallowed = edgesInScc.filter((edge) => !edge.allowCycle);
      if (disallowed.length > 0) {
        const offenders = disallowed
          .map((edge) => `${edge.syncName} (${edge.filePath})`)
          .sort();
        errors.push(
          `Dependency cycle detected among Concepts: ${unique.join(' -> ')} -> ${unique[0]}. ` +
            `Cycle not fully allowed. Offending synchronizations: ${offenders.join(', ')}.`
        );
      }
    }
  }

  if (errors.length > 0) {
    const deduped = [...new Set(errors)].sort();
    console.error(`Concept graph validation failed with ${deduped.length} error(s):`);
    for (const error of deduped) {
      console.error(`- ${error}`);
    }
    process.exit(1);
  }

  console.log('Concept graph validation passed.');
}

main();
