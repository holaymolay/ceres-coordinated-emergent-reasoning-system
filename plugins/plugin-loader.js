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
        let item = { [key]: parseScalar(rest) };
        const nextLine = nextNonEmptyLine(lines, i + 1);
        if (nextLine && nextLine.indent > indent) {
          const [child, nextIndex] = parseBlock(lines, i + 1, nextLine.indent);
          if (child && typeof child === 'object' && !Array.isArray(child)) {
            item = { ...item, ...child };
          }
          arr.push(item);
          i = nextIndex;
          continue;
        }
        arr.push(item);
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

function parseSimpleYaml(text) {
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

  const [value] = parseBlock(lines, 0, 0);
  return value;
}

function validatePlugin(plugin, registryPath) {
  const errors = [];
  const required = [
    'name',
    'version',
    'purpose',
    'compatibility',
    'hook_points',
    'constraints',
    'entrypoint',
    'type',
  ];

  for (const key of required) {
    if (!Object.prototype.hasOwnProperty.call(plugin, key)) {
      errors.push(`Missing required field '${key}'.`);
    }
  }

  if (!plugin.compatibility || typeof plugin.compatibility !== 'object') {
    errors.push('Compatibility must be an object.');
  } else {
    if (!plugin.compatibility.core_min || !plugin.compatibility.core_max) {
      errors.push('Compatibility must include core_min and core_max.');
    }
  }

  if (!Array.isArray(plugin.hook_points) || plugin.hook_points.length === 0) {
    errors.push('hook_points must be a non-empty array.');
  }

  if (!Array.isArray(plugin.constraints)) {
    errors.push('constraints must be an array.');
  }

  if (plugin.type !== 'analysis' && plugin.type !== 'suggestion') {
    errors.push("Plugin type must be 'analysis' or 'suggestion'.");
  }

  if (plugin.entrypoint && typeof plugin.entrypoint === 'string') {
    const entryPath = path.resolve(path.dirname(registryPath), '..', plugin.entrypoint);
    if (!fs.existsSync(entryPath)) {
      errors.push(`Entrypoint not found: ${plugin.entrypoint}`);
    }
  }

  return errors;
}

function loadRegistry(registryPath) {
  const content = fs.readFileSync(registryPath, 'utf8');
  return parseSimpleYaml(content);
}

function main() {
  const registryPath = process.argv[2] || path.join(process.cwd(), 'plugins', 'registry.yaml');

  if (!fs.existsSync(registryPath)) {
    console.error(`Plugin registry not found: ${registryPath}`);
    process.exit(1);
  }

  let registry;
  try {
    registry = loadRegistry(registryPath);
  } catch (err) {
    console.error(`Failed to parse plugin registry: ${err.message}`);
    process.exit(1);
  }

  if (!registry || typeof registry !== 'object') {
    console.error('Plugin registry must be a YAML object.');
    process.exit(1);
  }

  if (!Array.isArray(registry.plugins)) {
    console.error('Plugin registry must include a plugins array.');
    process.exit(1);
  }

  const errors = [];
  const pluginIndex = new Map();

  for (const plugin of registry.plugins) {
    if (!plugin || typeof plugin !== 'object') {
      errors.push('Invalid plugin entry in registry.');
      continue;
    }
    const pluginErrors = validatePlugin(plugin, registryPath);
    if (pluginIndex.has(plugin.name)) {
      pluginErrors.push(`Duplicate plugin name '${plugin.name}'.`);
    }
    pluginIndex.set(plugin.name, plugin);
    pluginErrors.forEach((error) => errors.push(`Plugin '${plugin.name}': ${error}`));
  }

  if (errors.length) {
    console.error(`Plugin registry validation failed with ${errors.length} error(s):`);
    errors.forEach((error) => console.error(`- ${error}`));
    process.exit(1);
  }

  const output = {
    version: registry.version || '1.0',
    plugins: registry.plugins,
  };

  process.stdout.write(`${JSON.stringify(output, null, 2)}\n`);
}

main();
