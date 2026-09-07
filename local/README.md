# IndexShelf local dependency stack

Copy `.env.example` to `.env` when local overrides are needed. The defaults use
non-default host ports so this stack does not collide with other Docker projects.

```powershell
./scripts/local-up.ps1
./scripts/local-down.ps1
```

The default profile starts only local dependencies. Published application images
are isolated behind the `published` profile and the separate
`compose.services.yaml` file.
