import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import YAML from 'yaml';
import { findSensitiveFields } from '../openapi/mobile/sensitiveContract.js';
import { findUnsecuredReservedOperations } from '../openapi/mobile/noAuthDrift.js';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const document = YAML.parse(fs.readFileSync(path.join(root, 'openapi/mobile/v1/openapi.yaml'), 'utf8'));

assert.equal(document.openapi, '3.1.0', 'OpenAPI 3.1 is required');
assert.ok(Array.isArray(document.servers) && document.servers.length > 0, 'At least one server is required');
assert.ok(document.servers.every(({ url }) => url.startsWith('https://')), 'All API servers must use HTTPS');
assert.ok(document.components?.securitySchemes?.bearerAuth, 'Bearer security scheme is required');
assert.deepEqual(findSensitiveFields(document.components.schemas), [], 'Sensitive schema fields are forbidden');
assert.deepEqual(findUnsecuredReservedOperations(document), [], 'Reserved public operations must declare security explicitly');
console.log('OpenAPI policy lint passed.');
