const RESERVED_PUBLIC_TAGS = new Set(['Identity', 'Product']);

export function findUnsecuredReservedOperations(document) {
  const violations = [];
  for (const [path, item] of Object.entries(document.paths ?? {})) {
    for (const [method, operation] of Object.entries(item)) {
      if (!['get', 'post', 'put', 'patch', 'delete'].includes(method)) continue;
      if ((operation.tags ?? []).some((tag) => RESERVED_PUBLIC_TAGS.has(tag)) && !operation.security) {
        violations.push(`${method.toUpperCase()} ${path} must declare security explicitly`);
      }
    }
  }
  return violations;
}
