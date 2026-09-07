namespace IndexShelf.Persistence;

public sealed record DatabaseConnectionOptions(string ConnectionString, bool IsMigrator)
{
    public static DatabaseConnectionOptions RuntimeFromEnvironment() => FromEnvironment("INDEXSHELF_RUNTIME_CONNECTION", false);
    public static DatabaseConnectionOptions MigratorFromEnvironment() => FromEnvironment("INDEXSHELF_MIGRATOR_CONNECTION", true);

    private static DatabaseConnectionOptions FromEnvironment(string name, bool isMigrator)
    {
        var value = Environment.GetEnvironmentVariable(name);
        if (string.IsNullOrWhiteSpace(value))
            throw new InvalidOperationException($"{name} must be configured.");
        return new DatabaseConnectionOptions(value, isMigrator);
    }
}
