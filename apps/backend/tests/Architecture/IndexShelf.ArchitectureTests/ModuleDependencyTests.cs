using System.Text.RegularExpressions;
using Xunit;

namespace IndexShelf.ArchitectureTests;

public sealed class ModuleDependencyTests
{
    [Fact]
    public void Modules_do_not_reference_another_module_source_or_entity_namespace()
    {
        foreach (var file in ArchitectureTestContext.ProductionFiles())
        {
            if (!file.Contains($"{Path.DirectorySeparatorChar}Modules{Path.DirectorySeparatorChar}", StringComparison.OrdinalIgnoreCase))
                continue;

            var source = File.ReadAllText(file);
            var currentModule = file.Split(Path.DirectorySeparatorChar, Path.AltDirectorySeparatorChar)
                .SkipWhile(segment => !segment.Equals("Modules", StringComparison.OrdinalIgnoreCase))
                .Skip(1)
                .FirstOrDefault();
            var moduleNames = Regexes.ModuleNamespace().Matches(source).Select(match => match.Groups[1].Value).Distinct();
            foreach (var module in moduleNames.Where(module => !module.Equals(currentModule, StringComparison.OrdinalIgnoreCase)))
            {
                var forbidden = new[]
                {
                    $"IndexShelf.Modules.{module}.Domain",
                    $"IndexShelf.Modules.{module}.Application",
                    $"IndexShelf.Modules.{module}.Presentation",
                };
                Assert.False(ArchitectureTestContext.ContainsForbiddenReference(source, forbidden), $"{file} references a module source namespace.");
            }
        }
    }

    [Fact]
    public void Module_contracts_are_the_only_explicit_cross_module_surface()
    {
        const string valid = "using IndexShelf.ModuleContracts.Bookmarks;";
        const string invalid = "using IndexShelf.Modules.Bookmarks.Domain;";

        Assert.False(ArchitectureTestContext.ContainsForbiddenReference(valid, ["IndexShelf.Modules.Bookmarks.Domain"]));
        Assert.True(ArchitectureTestContext.ContainsForbiddenReference(invalid, ["IndexShelf.Modules.Bookmarks.Domain"]));
    }

    [Fact]
    public void Module_projects_do_not_reference_each_other()
    {
        var moduleProjects = Directory.EnumerateFiles(
                Path.Combine(ArchitectureTestContext.BackendRoot, "src", "Modules"), "*.csproj", SearchOption.AllDirectories)
            .ToArray();
        foreach (var project in moduleProjects)
        {
            var current = Path.GetFileNameWithoutExtension(project).Replace("IndexShelf.Modules.", "", StringComparison.Ordinal);
            var references = File.ReadAllText(project);
            foreach (var other in moduleProjects.Where(candidate => !candidate.Equals(project, StringComparison.OrdinalIgnoreCase)))
            {
                var otherName = Path.GetFileNameWithoutExtension(other).Replace("IndexShelf.Modules.", "", StringComparison.Ordinal);
                Assert.DoesNotContain($"IndexShelf.Modules.{otherName}", references, StringComparison.OrdinalIgnoreCase);
            }
            Assert.Contains($"IndexShelf.Modules.{current}", references, StringComparison.OrdinalIgnoreCase);
        }
    }
}

internal static partial class Regexes
{
    [GeneratedRegex(@"IndexShelf\.Modules\.([A-Za-z0-9_]+)\.(?:Domain|Application|Presentation)")]
    public static partial Regex ModuleNamespace();
}
