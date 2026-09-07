using Microsoft.Extensions.DependencyInjection;

namespace IndexShelf.Modules.Bookmarks;

public static class DependencyInjection
{
    public static IServiceCollection AddBookmarksModule(this IServiceCollection services) => services;
}
