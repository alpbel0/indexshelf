using System.Text.RegularExpressions;

namespace IndexShelf.ArchitectureTests;

internal static partial class ArchitectureTestContext
{
    public static string BackendRoot => FindBackendRoot();

    public static IEnumerable<string> ProductionFiles(string extension = "*.cs") =>
        Directory.EnumerateFiles(Path.Combine(BackendRoot, "src"), extension, SearchOption.AllDirectories)
            .Where(path => !path.Contains($"{Path.DirectorySeparatorChar}bin{Path.DirectorySeparatorChar}", StringComparison.OrdinalIgnoreCase))
            .Where(path => !path.Contains($"{Path.DirectorySeparatorChar}obj{Path.DirectorySeparatorChar}", StringComparison.OrdinalIgnoreCase));

    public static bool ContainsForbiddenReference(string source, IEnumerable<string> namespaces) =>
        namespaces.Any(ns => Regex.IsMatch(source, $@"\b{Regex.Escape(ns)}(?:\.|\b)", RegexOptions.CultureInvariant));

    public static bool HasForbiddenFolder(string path) =>
        path.Split(Path.DirectorySeparatorChar, Path.AltDirectorySeparatorChar)
            .Any(segment => segment.Equals("utils", StringComparison.OrdinalIgnoreCase)
                || segment.Equals("helpers", StringComparison.OrdinalIgnoreCase)
                || segment.Equals("misc", StringComparison.OrdinalIgnoreCase));

    public static bool HasForbiddenTypeName(string source) =>
        Regex.IsMatch(source, @"\b(?:class|record|interface|struct)\s+\w*(?:Helper|Utils|Misc)\b", RegexOptions.CultureInvariant);

    private static string FindBackendRoot()
    {
        foreach (var start in new[] { Directory.GetCurrentDirectory(), AppContext.BaseDirectory })
        {
            var current = new DirectoryInfo(start);
            while (current is not null)
            {
                if (File.Exists(Path.Combine(current.FullName, "IndexShelf.Backend.slnx")))
                    return current.FullName;
                current = current.Parent;
            }
        }
        throw new DirectoryNotFoundException("Could not locate IndexShelf.Backend.slnx.");
    }
}
