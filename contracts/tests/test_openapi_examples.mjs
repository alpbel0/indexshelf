import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import YAML from 'yaml';
import Ajv from 'ajv';
import addFormats from 'ajv-formats';
import { syntheticProblemDetails } from '../openapi/mobile/syntheticExampleValues.js';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const document = YAML.parse(fs.readFileSync(path.join(root, 'openapi/mobile/v1/openapi.yaml'), 'utf8'));
const example = JSON.parse(fs.readFileSync(path.join(root, 'openapi/mobile/examples/problem-details.json'), 'utf8'));

test('OpenAPI document has secure versioned foundations', () => {
  assert.equal(document.openapi, '3.1.0');
  assert.equal(document.info.version, '1.0.0');
  assert.equal(document.components.securitySchemes.bearerAuth.scheme, 'bearer');
  assert.equal(document.components.parameters.CorrelationId.required, true);
  assert.equal(document.components.parameters.IdempotencyKey.required, true);
  assert.equal(document.components.parameters.AcceptLanguage.required, false);
});

test('synthetic Problem Details example validates against its schema', () => {
  const schema = { ...document.components.schemas.ProblemDetails };
  const ajv = new Ajv({ strict: false });
  addFormats(ajv);
  assert.equal(ajv.compile(schema)(example), true);
  assert.deepEqual(example, syntheticProblemDetails);
});
