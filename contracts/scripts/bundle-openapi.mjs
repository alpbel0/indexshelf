import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import YAML from 'yaml';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const sourcePath = path.join(root, 'openapi/mobile/v1/openapi.yaml');
const outputPath = path.join(root, 'dist/mobile-v1.yaml');
const document = YAML.parse(fs.readFileSync(sourcePath, 'utf8'));

assert.equal(document.openapi, '3.1.0');
assert.ok(document.components);
fs.mkdirSync(path.dirname(outputPath), { recursive: true });
fs.writeFileSync(outputPath, YAML.stringify(document), 'utf8');
console.log(`Created bundle at ${path.relative(root, outputPath)}.`);
