namespace IndexShelf.Application.Abstractions;

public sealed class HostRuntimeOptions
{
    public string Environment { get; init; } = "local";

    public void Validate()
    {
        if (Environment is not ("local" or "staging" or "production"))
        {
            throw new InvalidOperationException($"Unsupported environment '{Environment}'.");
        }
    }
}
