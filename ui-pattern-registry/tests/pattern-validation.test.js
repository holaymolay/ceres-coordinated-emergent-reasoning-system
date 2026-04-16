import assert from 'node:assert/strict';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import test from 'node:test';

import { validatePatterns } from '../scripts/validate-patterns.js';

const repoRoot = path.resolve(fileURLToPath(new URL('..', import.meta.url)));

function describeErrors(errors) {
  if (!errors || errors.length === 0) return '';
  return errors.map((entry) => `${entry.file ?? 'global'}: ${entry.message}`).join('\n');
}

test('registry patterns validate against schema', async () => {
  const result = await validatePatterns({ baseDir: repoRoot });
  assert.equal(result.ok, true, describeErrors(result.errors));
  assert.ok(result.filesChecked >= 5, 'Expected starter pattern set to be present');
});

test('invalid fixtures surface schema and duplicate errors', async () => {
  const result = await validatePatterns({
    baseDir: repoRoot,
    patternGlobs: ['tests/fixtures/invalid/*.yaml'],
    allowEmpty: false
  });

  assert.equal(result.ok, false, 'Expected invalid fixtures to fail validation');
  const messages = result.errors.map((entry) => `${entry.file ?? 'global'}: ${entry.message}`);
  assert.ok(messages.some((message) => message.includes('pattern_id')), 'Missing pattern_id should be flagged');
  assert.ok(
    messages.some((message) => message.includes('Duplicate pattern_id')),
    'Duplicate pattern_id should be reported'
  );
});
