#!/usr/bin/env node
'use strict';

const fs = require('node:fs');

function readInput() {
  const data = fs.readFileSync(0, 'utf8');
  return JSON.parse(data || '{}');
}

function toSnakeCase(value) {
  return String(value)
    .replace(/([a-z0-9])([A-Z])/g, '$1_$2')
    .replace(/\s+/g, '_')
    .replace(/-+/g, '_')
    .toLowerCase();
}

function normalizeKeys(obj) {
  if (Array.isArray(obj)) {
    return obj.map((item) => normalizeKeys(item));
  }
  if (obj && typeof obj === 'object') {
    const next = {};
    for (const [key, value] of Object.entries(obj)) {
      next[toSnakeCase(key)] = normalizeKeys(value);
    }
    return next;
  }
  return obj;
}

const payload = readInput();
const input = payload?.input?.payload ?? {};

const output = {
  normalized: normalizeKeys(input),
};

process.stdout.write(`${JSON.stringify(output)}\n`);
