using Microsoft.EntityFrameworkCore;
using IndexShelf.Persistence.Context;

namespace IndexShelf.Persistence.Conventions;

public static class LogicalSchemaConvention
{
    public static void Apply(ModelBuilder modelBuilder)
    {
        foreach (var entity in modelBuilder.Model.GetEntityTypes())
        {
            var module = entity.ClrType.Namespace?.Split('.')
                .SkipWhile(segment => !segment.Equals("Modules", StringComparison.Ordinal))
                .Skip(1).FirstOrDefault();
            var schema = module switch
            {
                "Identity" => SchemaNames.Identity,
                "Bookmarks" => SchemaNames.Bookmarks,
                "Reminders" => SchemaNames.Reminders,
                "Search" => SchemaNames.Search,
                "Operations" => SchemaNames.Operations,
                _ => null
            };
            if (schema is not null)
                entity.SetSchema(schema);
        }
    }
}
