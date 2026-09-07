const SENSITIVE_NAMES = /(?:password|secret|token|cookie|credential|api[-_]?key|proxy)/i;

export function findSensitiveFields(value, path = []) {
  if (!value || typeof value !== 'object') return [];
  const fields = [];
  for (const [key, child] of Object.entries(value)) {
    const childPath = [...path, key];
    if (SENSITIVE_NAMES.test(key)) fields.push(childPath.join('.'));
    fields.push(...findSensitiveFields(child, childPath));
  }
  return fields;
}
