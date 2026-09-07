using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.DependencyInjection;
using Npgsql;
using IndexShelf.Persistence.Context;

namespace IndexShelf.Persistence;

public static class DependencyInjection
{
    public static IServiceCollection AddIndexShelfRuntimePersistence(this IServiceCollection services)
        => services.AddIndexShelfPersistence(DatabaseConnectionOptions.RuntimeFromEnvironment());

    public static IServiceCollection AddIndexShelfPersistence(this IServiceCollection services, DatabaseConnectionOptions options)
    {
        if (options.IsMigrator)
            throw new ArgumentException("Runtime persistence registration cannot use migrator credentials.", nameof(options));

        var dataSource = new NpgsqlDataSourceBuilder(options.ConnectionString).Build();
        services.AddDbContext<IndexShelfDbContext>(builder => builder.UseNpgsql(dataSource));
        return services;
    }
}
