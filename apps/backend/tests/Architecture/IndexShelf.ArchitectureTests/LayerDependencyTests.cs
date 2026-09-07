using System.Text.RegularExpressions;
using Xunit;

namespace IndexShelf.ArchitectureTests;

public sealed class LayerDependencyTests
{
    [Fact]
    public void Domain_does_not_reference_outer_layers_or_infrastructure_providers()
    {
        foreach (var file in ArchitectureTestContext.ProductionFiles().Where(IsUnder("Domain")))
        {
            Assert.False(
                ArchitectureTestContext.ContainsForbiddenReference(File.ReadAllText(file), ["Application", "Presentation", "Infrastructure", "Microsoft.AspNetCore", "Microsoft.EntityFrameworkCore"]),
                $"{file} contains an outer-layer or provider reference.");
        }
    }

    [Fact]
    public void Presentation_does_not_access_persistence_directly()
    {
        foreach (var file in ArchitectureTestContext.ProductionFiles().Where(IsUnder("Presentation")))
        {
            Assert.False(
                ArchitectureTestContext.ContainsForbiddenReference(File.ReadAllText(file), ["IndexShelf.Persistence", "Microsoft.EntityFrameworkCore"]),
                $"{file} accesses persistence directly.");
        }
    }

    [Fact]
    public void There_is_at_most_one_db_context_and_one_root_solution()
    {
        var dbContextCount = ArchitectureTestContext.ProductionFiles()
            .Select(File.ReadAllText)
            .Sum(source => Regexes.DbContext().Count(source));
        var solutionCount = Directory.EnumerateFiles(ArchitectureTestContext.BackendRoot, "*.slnx").Count();

        Assert.InRange(dbContextCount, 0, 1);
        Assert.Equal(1, solutionCount);
    }

    private static Func<string, bool> IsUnder(string directory) => path =>
        path.Split(Path.DirectorySeparatorChar, Path.AltDirectorySeparatorChar).Contains(directory, StringComparer.OrdinalIgnoreCase);
}

internal static partial class Regexes
{
    [GeneratedRegex(@"\bclass\s+\w*DbContext\b")]
    public static partial Regex DbContext();
}
