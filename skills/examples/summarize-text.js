#!/usr/bin/env node
'use strict';

const fs = require('node:fs');

function readInput() {
  const data = fs.readFileSync(0, 'utf8');
  return JSON.parse(data || '{}');
}

function summarize(text) {
  const cleaned = String(text || '').trim().replace(/\s+/g, ' ');
  if (!cleaned) {
    return '';
  }
  const words = cleaned.split(' ');
  if (words.length <= 20) {
    return cleaned;
  }
  return `${words.slice(0, 20).join(' ')}...`;
}

const payload = readInput();
const text = payload?.input?.text ?? '';

const output = {
  summary: summarize(text),
};

process.stdout.write(`${JSON.stringify(output)}\n`);
