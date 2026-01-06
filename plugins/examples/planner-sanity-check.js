#!/usr/bin/env node
'use strict';

const fs = require('node:fs');

function readInput() {
  const data = fs.readFileSync(0, 'utf8');
  return JSON.parse(data || '{}');
}

const payload = readInput();
const tasks = payload?.input?.tasks || [];

const warnings = [];
if (!Array.isArray(tasks) || tasks.length === 0) {
  warnings.push('No tasks provided to plugin input.');
} else {
  const duplicates = new Set();
  const seen = new Set();
  for (const task of tasks) {
    const id = task && task.id ? String(task.id) : null;
    if (!id) {
      warnings.push('Task missing id.');
      continue;
    }
    if (seen.has(id)) {
      duplicates.add(id);
    }
    seen.add(id);
  }
  if (duplicates.size) {
    warnings.push(`Duplicate task ids detected: ${Array.from(duplicates).join(', ')}`);
  }
}

const output = {
  warnings,
  count: Array.isArray(tasks) ? tasks.length : 0,
};

process.stdout.write(`${JSON.stringify(output)}\n`);
