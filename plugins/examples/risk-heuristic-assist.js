#!/usr/bin/env node
'use strict';

const fs = require('node:fs');

function readInput() {
  const data = fs.readFileSync(0, 'utf8');
  return JSON.parse(data || '{}');
}

const payload = readInput();
const notes = [];

const tasks = payload?.input?.tasks || [];
if (Array.isArray(tasks)) {
  for (const task of tasks) {
    if (task && typeof task.description === 'string') {
      if (task.description.toLowerCase().includes('deploy')) {
        notes.push(`Task '${task.id || '<unknown>'}' mentions deploy; ensure rollback plan exists.`);
      }
      if (task.description.toLowerCase().includes('delete')) {
        notes.push(`Task '${task.id || '<unknown>'}' mentions delete; confirm data retention rules.`);
      }
    }
  }
}

const output = {
  suggestions: notes,
  guidance: 'Non-binding risk flags for human review only.',
};

process.stdout.write(`${JSON.stringify(output)}\n`);
