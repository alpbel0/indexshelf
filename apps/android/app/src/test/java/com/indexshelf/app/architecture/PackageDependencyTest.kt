package com.indexshelf.app.architecture

import java.nio.file.Files
import java.nio.file.Path
import kotlin.io.path.readText
import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Test

class PackageDependencyTest {
    @Test
    fun currentSourceHasNoPackageBoundaryViolations() {
        val root = Path.of("src/main/java")
        assertTrue("Android source root does not exist: $root", Files.exists(root))
        val sources = Files.walk(root).use { paths ->
            paths.filter { it.toString().endsWith(".kt") }.toList().associateWith { it.readText() }
        }.mapKeys { it.key.toString() }

        assertTrue(
            "Package boundary violations: ${PackageArchitectureRules.violations(sources)}",
            PackageArchitectureRules.violations(sources).isEmpty(),
        )
    }

    @Test
    fun presentationToDataViolationIsRejected() {
        val sources = mapOf(
            "presentation/BookmarkScreen.kt" to
                "package com.indexshelf.feature.bookmarks.presentation\n" +
                    "import com.indexshelf.feature.bookmarks.data.BookmarkRepository",
        )

        assertEquals(1, PackageArchitectureRules.violations(sources).size)
    }

    @Test
    fun crossFeatureImplementationViolationIsRejected() {
        val sources = mapOf(
            "bookmarks/Screen.kt" to
                "package com.indexshelf.feature.bookmarks.domain\n" +
                    "import com.indexshelf.feature.search.data.SearchRepository",
        )

        val violations = PackageArchitectureRules.violations(sources)
        assertTrue(
            "Cross-feature implementation import was not rejected: $violations",
            violations.any { it.contains("another feature implementation") },
        )
    }

    @Test
    fun androidComponentBusinessLogicViolationIsRejected() {
        val sources = mapOf(
            "MainActivity.kt" to
                "class MainActivity : ComponentActivity() { private val repository: BookmarkRepository? = null }",
        )

        assertEquals(1, PackageArchitectureRules.violations(sources).size)
    }

    @Test
    fun domainToDataViolationIsRejected() {
        val sources = mapOf(
            "domain/Bookmark.kt" to
                "package com.indexshelf.feature.bookmarks.domain\n" +
                    "import com.indexshelf.feature.bookmarks.data.BookmarkEntity",
        )

        assertEquals(1, PackageArchitectureRules.violations(sources).size)
    }

    @Test
    fun modelAliasViolationIsRejected() {
        val sources = mapOf(
            "domain/Bookmark.kt" to
                "package com.indexshelf.feature.bookmarks.domain\n" +
                    "typealias BookmarkDto = BookmarkEntity",
        )

        assertEquals(1, PackageArchitectureRules.violations(sources).size)
    }
}
