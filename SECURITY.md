# Security Policy

## Reporting a vulnerability

Do not open a public issue for a suspected security vulnerability. Contact the
project owner privately with a description, reproduction steps, and impact.

Never include real credentials, personal data, provider responses, or production
access details in an issue, pull request, log, fixture, or documentation file.

## Security baseline

- Secrets belong in local ignored configuration or an external secret manager.
- User files and remote URLs are untrusted input.
- Generated artifacts, database dumps, and Terraform state are not committed.
- Authentication, authorization, SSRF protection, retention, and deletion must
  be verified by tests before production use.
