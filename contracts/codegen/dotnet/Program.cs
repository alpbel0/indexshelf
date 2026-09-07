using NJsonSchema;
using NJsonSchema.CodeGeneration.CSharp;

if (args.Length != 2)
{
    Console.Error.WriteLine("Usage: IndexShelf.ContractCodegen <schema-root> <output-directory>");
    return 2;
}

var schemaRoot = Path.GetFullPath(args[0]);
var outputDirectory = Path.GetFullPath(args[1]);
Directory.CreateDirectory(outputDirectory);

foreach (var schemaPath in Directory.EnumerateFiles(schemaRoot, "*.schema.json", SearchOption.AllDirectories).Order())
{
    var schema = await JsonSchema.FromFileAsync(schemaPath);
    var className = Path.GetFileNameWithoutExtension(Path.GetFileNameWithoutExtension(schemaPath))
        .Split('-', StringSplitOptions.RemoveEmptyEntries)
        .Select(part => char.ToUpperInvariant(part[0]) + part[1..])
        .Aggregate(string.Concat);
    schema.Title = className;
        var generator = new CSharpGenerator(schema, new CSharpGeneratorSettings { Namespace = $"IndexShelf.Contracts.Generated.{className}" });
    var outputPath = Path.Combine(outputDirectory, $"{className}.g.cs");
    await File.WriteAllTextAsync(outputPath, generator.GenerateFile());
}

Console.WriteLine($"Generated {Directory.GetFiles(outputDirectory, "*.g.cs").Length} C# files.");
return 0;
