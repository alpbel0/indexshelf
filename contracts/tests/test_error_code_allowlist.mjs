import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import YAML from 'yaml';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const document = YAML.parse(fs.readFileSync(path.join(root, 'openapi/mobile/v1/openapi.yaml'), 'utf8'));
const allowed = document.components.schemas.StableErrorCode.enum;

test('Problem Details and stable error code component share one allowlist', () => {
  assert.deepEqual(document.components.schemas.ProblemDetails.properties.code.enum, allowed);
});
