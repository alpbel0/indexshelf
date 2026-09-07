namespace IndexShelf.Persistence.Context;

public static class SchemaNames
{
    public const string Identity = "identity";
    public const string Bookmarks = "bookmarks";
    public const string Reminders = "reminders";
    public const string Search = "search";
    public const string Operations = "operations";

    public static readonly IReadOnlyList<string> Mvp =
        [Identity, Bookmarks, Reminders, Search, Operations];
}
