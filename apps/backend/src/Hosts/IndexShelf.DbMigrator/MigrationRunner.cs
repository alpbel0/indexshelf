namespace IndexShelf.DbMigrator;

using Microsoft.EntityFrameworkCore;
using Npgsql;
using IndexShelf.Persistence;
using IndexShelf.Persistence.Context;

public static class MigrationRunner
{
    private const long MigrationLockKey = 716_298_401;

    public static async Task RunAsync(CancellationToken cancellationToken = default)
    {
        var options = DatabaseConnectionOptions.MigratorFromEnvironment();
        await using var connection = new NpgsqlConnection(options.ConnectionString);
        await connection.OpenAsync(cancellationToken);
        await using var lockCommand = new NpgsqlCommand("select pg_try_advisory_lock(@key);", connection);
        lockCommand.Parameters.AddWithValue("key", MigrationLockKey);
        var acquired = (bool)(await lockCommand.ExecuteScalarAsync(cancellationToken) ?? false);
        if (!acquired)
            throw new InvalidOperationException("Could not acquire migration lock: another migrator instance is running.");
        try
        {
            var dbOptions = new DbContextOptionsBuilder<IndexShelfDbContext>()
                .UseNpgsql(connection, npgsql => npgsql.MigrationsHistoryTable("__ef_migrations_history", "public"))
                .Options;
            await using var db = new IndexShelfDbContext(dbOptions);
            await db.Database.MigrateAsync(cancellationToken);
        }
        finally
        {
            await using var unlockCommand = new NpgsqlCommand("select pg_advisory_unlock(@key);", connection);
            unlockCommand.Parameters.AddWithValue("key", MigrationLockKey);
            await unlockCommand.ExecuteNonQueryAsync(CancellationToken.None);
        }
    }
}
