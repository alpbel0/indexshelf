using Microsoft.EntityFrameworkCore;

namespace IndexShelf.Persistence.Conventions;

public static class UtcDateTimeConvention
{
    public static void Apply(ModelBuilder modelBuilder)
    {
        foreach (var property in modelBuilder.Model.GetEntityTypes().SelectMany(entity => entity.GetProperties()))
        {
            if (property.ClrType == typeof(DateTime) || property.ClrType == typeof(DateTime?))
                property.SetColumnType("timestamp with time zone");
            else if (property.ClrType == typeof(DateTimeOffset) || property.ClrType == typeof(DateTimeOffset?))
                property.SetColumnType("timestamp with time zone");
        }
    }
}
