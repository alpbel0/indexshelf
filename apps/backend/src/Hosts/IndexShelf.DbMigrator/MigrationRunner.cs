namespace IndexShelf.DbMigrator;

public static class MigrationRunner
{
    public static Task RunAsync(CancellationToken cancellationToken = default)
        => Task.FromException(new InvalidOperationException(
            "Database migration is not configured yet; no migration was applied."));
}
