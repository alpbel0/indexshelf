# Backend

The backend targets .NET 10 LTS. `IndexShelf.Backend.slnx` is the only
authoritative solution. Application hosts and product modules are added in
later bootstrap tasks; the current solution contains the first buildable
SharedKernel boundary so restore/build is meaningful from the start.

The .NET SDK pins format, analyzers, and test commands through `global.json`.
The local tool manifest pins the external `dotnet-ef` command used by later
migration tasks.

Run from this directory:

```text
dotnet restore
dotnet build --no-restore
```

## Local containers

Run the backend image bake from the repository root so the relative build context resolves
correctly:

```text
docker buildx bake --allow=fs.read=C:\Users -f apps/backend/build/docker-bake.hcl
```

The API uses custom port `18080`; publish it explicitly when needed. Worker and migrator do not
publish host ports.
