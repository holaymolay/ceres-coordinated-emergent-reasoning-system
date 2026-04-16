#!/usr/bin/env node
import fs from 'node:fs/promises';
import path from 'node:path';
import process from 'node:process';
import { fileURLToPath } from 'node:url';
import { glob } from 'glob';
import Ajv from 'ajv';
import addFormats from 'ajv-formats';
import YAML from 'yaml';

const DEFAULT_GLOBS = ['patterns/**/*.{yml,yaml,json}'];

function parsePattern(rawContent, filePath) {
  const extension = path.extname(filePath).toLowerCase();
  if (extension === '.json') {
    return JSON.parse(rawContent);
  }
  return YAML.parse(rawContent);
}

function formatAjvError(error) {
  const location = error.instancePath || error.schemaPath || '';
  return `${location} ${error.message ?? ''}`.trim();
}

async function loadSchema(schemaPath) {
  const raw = await fs.readFile(schemaPath, 'utf8');
  return JSON.parse(raw);
}

export async function validatePatterns(options = {}) {
  const {
    baseDir = process.cwd(),
    patternGlobs = DEFAULT_GLOBS,
    schemaPath = path.join(baseDir, 'schemas/pattern.schema.json'),
    allowEmpty = false
  } = options;

  const schema = await loadSchema(schemaPath);
  const ajv = new Ajv({ allErrors: true, strict: true });
  addFormats(ajv);
  const validate = ajv.compile(schema);

  const resolvedGlobs = Array.isArray(patternGlobs) ? patternGlobs : [patternGlobs];
  const fileLists = await Promise.all(
    resolvedGlobs.map((pattern) => glob(pattern, { cwd: baseDir, absolute: true, nodir: true }))
  );
  const patternFiles = fileLists.flat();

  const errors = [];
  const seenIds = new Map();

  if (patternFiles.length === 0 && !allowEmpty) {
    errors.push({ file: null, message: 'No pattern files found.', details: [] });
  }

  for (const absolutePath of patternFiles) {
    const relativePath = path.relative(baseDir, absolutePath);
    let parsed;
    try {
      const raw = await fs.readFile(absolutePath, 'utf8');
      parsed = parsePattern(raw, absolutePath);
    } catch (error) {
      errors.push({ file: relativePath, message: 'Parse error', details: [error.message] });
      continue;
    }

    const patternId = parsed?.pattern_id;
    if (!patternId) {
      errors.push({ file: relativePath, message: 'pattern_id is missing', details: [] });
    } else if (seenIds.has(patternId)) {
      errors.push({
        file: relativePath,
        message: `Duplicate pattern_id '${patternId}' also seen in ${seenIds.get(patternId)}`,
        details: []
      });
    } else {
      seenIds.set(patternId, relativePath);
    }

    const valid = validate(parsed);
    if (!valid) {
      const formatted = validate.errors?.map(formatAjvError) ?? ['Unknown validation error'];
      errors.push({ file: relativePath, message: 'Schema validation failed', details: formatted });
    }
  }

  return { ok: errors.length === 0, errors, filesChecked: patternFiles.length };
}

function formatErrors(errors) {
  return errors
    .map((entry) => {
      const header = entry.file ? `${entry.file}: ${entry.message}` : entry.message;
      if (entry.details && entry.details.length > 0) {
        const detailLines = entry.details.map((detail) => `    - ${detail}`).join('\n');
        return `${header}\n${detailLines}`;
      }
      return header;
    })
    .join('\n');
}

async function runCli() {
  const result = await validatePatterns();
  if (!result.ok) {
    console.error('Pattern validation failed:');
    console.error(formatErrors(result.errors));
    process.exitCode = 1;
    return;
  }
  console.log(`Validated ${result.filesChecked} pattern file(s).`);
}

const currentFile = fileURLToPath(import.meta.url);
const invokedPath = process.argv[1] ? path.resolve(process.argv[1]) : null;
if (invokedPath && invokedPath === currentFile) {
  runCli().catch((error) => {
    console.error('Pattern validation crashed:', error);
    process.exitCode = 1;
  });
}
