using Microsoft.EntityFrameworkCore;
using Npgsql;

namespace IndexShelf.Persistence.Context;

public sealed class IndexShelfDbContextFactory
{
    public static IndexShelfDbContext CreateDbContext(string[] args)
    {
        var connectionString = Environment.GetEnvironmentVariable("INDEXSHELF_MIGRATOR_CONNECTION")
            ?? Environment.GetEnvironmentVariable("INDEXSHELF_RUNTIME_CONNECTION")
            ?? "Host=localhost;Port=55433;Database=indexshelf;Username=indexshelf_product_migrator;Password=indexshelf_product_migrator_dummy";
        var options = new DbContextOptionsBuilder<IndexShelfDbContext>()
            .UseNpgsql(new NpgsqlDataSourceBuilder(connectionString).Build(), npgsql => npgsql.MigrationsHistoryTable("__ef_migrations_history", "public"))
            .Options;
        return new IndexShelfDbContext(options);
    }
}
