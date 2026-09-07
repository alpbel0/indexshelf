namespace IndexShelf.SharedKernel.Domain;

/// <summary>Base identity contract for backend domain entities.</summary>
public abstract class Entity<TId>(TId id)
    where TId : notnull
{
    public TId Id { get; } = id;
}
