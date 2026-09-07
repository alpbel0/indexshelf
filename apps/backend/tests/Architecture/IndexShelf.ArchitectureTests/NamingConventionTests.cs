using Xunit;

namespace IndexShelf.ArchitectureTests;

public sealed class NamingConventionTests
{
    [Fact]
    public void Generic_utility_folders_are_not_allowed()
    {
        var violations = ArchitectureTestContext.ProductionFiles()
            .Where(ArchitectureTestContext.HasForbiddenFolder)
            .ToArray();

        Assert.Empty(violations);
    }

    [Fact]
    public void Generic_utility_type_names_are_not_allowed()
    {
        var violations = ArchitectureTestContext.ProductionFiles()
            .Where(path => ArchitectureTestContext.HasForbiddenTypeName(File.ReadAllText(path)))
            .ToArray();

        Assert.Empty(violations);
    }

    [Fact]
    public void Negative_fixture_proves_forbidden_folder_detection()
    {
        Assert.False(ArchitectureTestContext.HasForbiddenFolder(Path.Combine("src", "Common", "file.cs")));
        Assert.True(ArchitectureTestContext.HasForbiddenFolder(Path.Combine("src", "Helpers", "file.cs")));
        Assert.True(ArchitectureTestContext.HasForbiddenFolder(Path.Combine("src", "Utils", "file.cs")));
        Assert.True(ArchitectureTestContext.HasForbiddenFolder(Path.Combine("src", "Misc", "file.cs")));
        Assert.True(ArchitectureTestContext.HasForbiddenTypeName("class BookmarkHelper {}"));
        Assert.True(ArchitectureTestContext.HasForbiddenTypeName("record SearchUtils;"));
        Assert.True(ArchitectureTestContext.HasForbiddenTypeName("interface PipelineMisc {}"));
    }
}
