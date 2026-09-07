const SENSITIVE_NAMES = /(password|secret|token|cookie|credential|api[-_]?key|proxy)/i;

module.exports = {
  noSensitiveProperties(targetVal) {
    if (!targetVal || typeof targetVal !== 'object') return [];
    return Object.keys(targetVal)
      .filter((key) => SENSITIVE_NAMES.test(key))
      .map((key) => ({ message: `Sensitive field '${key}' is not allowed in mobile contracts.` }));
  },
};
