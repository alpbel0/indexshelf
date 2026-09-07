# IndexShelf

IndexShelf is a contract-first product with three deliberately separate
application areas:

- `apps/backend`: the .NET product backend and background hosts.
- `apps/data`: Python workers for extraction and media processing.
- `apps/android`: Kotlin/Jetpack Compose mobile client.
- `contracts`: versioned OpenAPI and JSON Schema boundaries.
- `local`: local-only PostgreSQL, RabbitMQ, Valkey, MinIO, and provider mocks.
- `e2e`: black-box cross-service acceptance tests.

Backend and Data never import each other's source code or database models. The
mobile client talks to the Backend public API and short-lived object URLs only.
Large content crosses service boundaries through opaque references, not inline
payloads.

## Development

This project uses a direct-to-`main` workflow while it is maintained by one
developer. Keep commits small and independently buildable. Validate locally
with the root checks before sharing a change. Automated CI is intentionally
deferred until after the MVP.

Tool versions are declared in `mise.toml`; application-specific toolchains may
also pin their own versions under `apps/*` or `contracts/`.

## Repository rules

- Never commit secrets, personal data, provider response dumps, database dumps,
  generated source, build output, or infrastructure state.
- Do not create a second root roadmap or duplicate an authoritative decision.
- `docs/` is a workspace-local, Git-ignored decision and roadmap tree for this
  phase. The authoritative docs remain available in the local workspace.
- Do not add a vague shared runtime `common` package between applications.
- Production credentials and production data must never be used by local or E2E
  tests.

## License

Released under the [MIT License](LICENSE).
