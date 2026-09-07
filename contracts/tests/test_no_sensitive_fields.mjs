import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import YAML from 'yaml';
import { findSensitiveFields } from '../openapi/mobile/sensitiveContract.js';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const document = YAML.parse(fs.readFileSync(path.join(root, 'openapi/mobile/v1/openapi.yaml'), 'utf8'));
const example = JSON.parse(fs.readFileSync(path.join(root, 'openapi/mobile/examples/problem-details.json'), 'utf8'));

test('OpenAPI schemas and synthetic examples contain no sensitive-shaped fields', () => {
  assert.deepEqual(findSensitiveFields(document.components.schemas), []);
  assert.deepEqual(findSensitiveFields(example), []);
});
