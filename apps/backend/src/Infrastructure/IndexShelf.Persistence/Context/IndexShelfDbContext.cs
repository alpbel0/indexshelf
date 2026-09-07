using Microsoft.EntityFrameworkCore;
using IndexShelf.Persistence.Conventions;

namespace IndexShelf.Persistence.Context;

public sealed class IndexShelfDbContext(DbContextOptions<IndexShelfDbContext> options) : DbContext(options)
{
    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.ApplyConfigurationsFromAssembly(typeof(IndexShelfDbContext).Assembly);
        LogicalSchemaConvention.Apply(modelBuilder);
        SnakeCaseNamingConvention.Apply(modelBuilder);
        UtcDateTimeConvention.Apply(modelBuilder);
        PersistenceConventions.Apply(modelBuilder);
        base.OnModelCreating(modelBuilder);
    }
}
