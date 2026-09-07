package com.indexshelf.app.core.localization

import java.io.File
import javax.xml.parsers.DocumentBuilderFactory
import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Test

class TranslationCompletenessTest {
    @Test
    fun englishAndTurkishStringKeysAndPlaceholdersMatch() {
        val english = parse(File("src/main/res/values/strings.xml"))
        val turkish = parse(File("src/main/res/values-tr/strings.xml"))
        assertEquals(english.keys, turkish.keys)
        english.forEach { (key, placeholders) ->
            assertEquals("Placeholder mismatch for $key", placeholders, turkish[key])
        }
    }

    @Test
    fun supportedLocalesAreDeclaredAndTranslationResourcesExist() {
        val config = File("src/main/res/xml/locales_config.xml").readText()
        assertTrue(config.contains("android:name=\"en\""))
        assertTrue(config.contains("android:name=\"tr\""))
        assertTrue(File("src/main/res/values-tr/strings.xml").exists())
        assertTrue(File("src/main/AndroidManifest.xml").readText().contains("android:supportsRtl=\"true\""))
        assertTrue(File("build.gradle.kts").readText().contains("isPseudoLocalesEnabled = true"))
    }

    @Test
    fun userFacingComposeTextDoesNotUseStringLiterals() {
        val sourceRoot = File("src/main/java")
        val forbidden = sourceRoot.walkTopDown()
            .filter { it.isFile && it.extension == "kt" }
            .flatMap { file ->
                Regex("(?s)\\b(Text|stringResource)\\s*\\([^)]*\"[^\"]+\"").findAll(file.readText())
                    .map { "${file.path}:${it.value}" }
            }
            .toList()
        assertTrue("User-facing string literals found: $forbidden", forbidden.isEmpty())
    }

    private fun parse(file: File): Map<String, Set<String>> {
        val document = DocumentBuilderFactory.newInstance().newDocumentBuilder().parse(file)
        val entries = mutableMapOf<String, Set<String>>()
        document.getElementsByTagName("string").let { nodes ->
            (0 until nodes.length).forEach { index ->
                val node = nodes.item(index)
                entries[node.attributes.getNamedItem("name").nodeValue] =
                    Regex("%[0-9$]*[sd]").findAll(node.textContent).map { it.value }.toSet()
            }
        }
        document.getElementsByTagName("plurals").let { nodes ->
            (0 until nodes.length).forEach { index ->
                val node = nodes.item(index)
                entries[node.attributes.getNamedItem("name").nodeValue] =
                    Regex("%[0-9$]*[sd]").findAll(node.textContent).map { it.value }.toSet()
            }
        }
        return entries
    }
}
