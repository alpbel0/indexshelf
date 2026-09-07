using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata;

namespace IndexShelf.Persistence.Conventions;

public static class PersistenceConventions
{
    public static void Apply(ModelBuilder modelBuilder)
    {
        foreach (var entity in modelBuilder.Model.GetEntityTypes())
        {
            foreach (var property in entity.GetProperties())
            {
                if (property.ClrType == typeof(Guid) && property.IsPrimaryKey())
                {
                    property.ValueGenerated = ValueGenerated.OnAdd;
                    property.SetValueGeneratorFactory((_, _) => new UuidV7ValueGenerator());
                }
                if (property.Name.Equals("Version", StringComparison.Ordinal) && property.ClrType == typeof(long))
                {
                    property.IsConcurrencyToken = true;
                    property.SetDefaultValue(1L);
                }
            }
        }
    }
}
