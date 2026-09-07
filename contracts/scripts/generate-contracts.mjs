import fs from 'node:fs';
import crypto from 'node:crypto';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { parse } from 'yaml';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const manifest = parse(fs.readFileSync(path.join(root, 'manifest.yaml'), 'utf8'));
const generated = path.join(root, 'generated');
fs.rmSync(generated, { recursive: true, force: true });
fs.mkdirSync(path.join(generated, 'python'), { recursive: true });
fs.mkdirSync(path.join(generated, 'dotnet'), { recursive: true });

function run(command, args, options = {}) {
  const executable = command;
  const result = spawnSync(executable, args, {
    cwd: root,
    stdio: 'inherit',
    shell: process.platform === 'win32',
    ...options,
  });
  if (result.status !== 0) throw new Error(`${command} failed with status ${result.status}`);
}

run('npm', ['run', 'generate:kotlin', '--', '-o', 'generated/kotlin']);
const dataSchemaFiles = fs.readdirSync(path.join(root, 'jsonschema/data/v1'), { recursive: true })
  .filter((entry) => entry.endsWith('.schema.json'))
  .sort();
for (const schemaFile of dataSchemaFiles) {
  const inputPath = path.posix.join('jsonschema/data/v1', schemaFile.split(path.sep).join('/'));
  const baseArgs = ['run', 'datamodel-codegen', '--input', inputPath, '--input-file-type', 'jsonschema', '--output-model-type', 'pydantic_v2.BaseModel', '--use-schema-description', '--use-standard-collections', '--disable-timestamp'];
  const moduleName = path.basename(schemaFile, '.schema.json').replaceAll('-', '_');
  const moduleDirectory = path.join(generated, 'python', moduleName);
  fs.mkdirSync(moduleDirectory, { recursive: true });
  try {
    run('uv', [...baseArgs, '--output', `generated/python/${moduleName}/models.py`]);
  } catch {
    run('uv', [...baseArgs, '--output', `generated/python/${moduleName}`]);
  }
}
run('uv', ['run', 'python', 'scripts/smoke-python.py']);
run('dotnet', ['run', '--project', 'codegen/dotnet/IndexShelf.ContractCodegen.csproj', '--', 'jsonschema/data/v1', 'generated/dotnet']);
run('dotnet', ['build', 'codegen/dotnet/smoke/IndexShelf.ContractCodegen.Smoke.csproj']);
const gradleWrapper = process.platform === 'win32' ? 'codegen/kotlin/smoke/gradlew.bat' : 'codegen/kotlin/smoke/gradlew';
run(path.join(root, gradleWrapper), ['-p', 'codegen/kotlin/smoke', 'compileKotlin']);

const sourceFiles = [
  'openapi/mobile/v1/openapi.yaml',
  ...fs.readdirSync(path.join(root, 'jsonschema/data/v1'), { recursive: true })
    .filter((entry) => entry.endsWith('.schema.json'))
    .map((entry) => path.posix.join('jsonschema/data/v1', entry.split(path.sep).join('/'))),
].sort();
const sourceChecksums = Object.fromEntries(sourceFiles.map((relativePath) => {
  const digest = crypto.createHash('sha256').update(fs.readFileSync(path.join(root, relativePath))).digest('hex');
  return [relativePath, digest];
}));
fs.writeFileSync(path.join(generated, 'codegen-manifest.json'), `${JSON.stringify({
  manifestVersion: manifest.codegen.manifestVersion,
  contractManifest: '../manifest.yaml',
  generatedRoot: 'generated',
  sourceChecksums,
  provenance: {
    ...manifest.codegen.provenance,
  },
}, null, 2)}\n`);
console.log('Contract codegen completed in contracts/generated.');
