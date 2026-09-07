import test from 'node:test';
import assert from 'node:assert/strict';
import YAML from 'yaml';
import { findUnsecuredReservedOperations } from '../openapi/mobile/noAuthDrift.js';

test('reserved Identity and Product operations cannot silently drift to anonymous access', () => {
  const secured = YAML.parse('paths:\n  /identity: \n    get:\n      tags: [Identity]\n      security: [{ bearerAuth: [] }]');
  const unsecured = YAML.parse('paths:\n  /identity: \n    get:\n      tags: [Identity]');
  assert.deepEqual(findUnsecuredReservedOperations(secured), []);
  assert.deepEqual(findUnsecuredReservedOperations(unsecured), ['GET /identity must declare security explicitly']);
});
