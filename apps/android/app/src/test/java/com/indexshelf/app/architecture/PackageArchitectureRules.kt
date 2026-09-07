package com.indexshelf.app.architecture

internal object PackageArchitectureRules {
    private val layers = setOf("presentation", "domain", "data", "core")
    private val componentTypes = setOf("Activity", "Service", "Receiver")

    @Suppress("CyclomaticComplexMethod")
    fun violations(sources: Map<String, String>): List<String> =
        sources.flatMap { (path, source) ->
            val packageName = packageName(source)
            val imports = source.lineSequence()
                .map(String::trim)
                .filter { it.startsWith("import ") }
                .map { it.removePrefix("import ").substringBefore(" ") }
                .toList()
            val currentLayer = packageName.split(".").firstOrNull { it in layers }
            buildList {
                if (currentLayer == "presentation" && imports.any { it.contains(".data.") }) {
                    add("$path: presentation imports data")
                }
                if (currentLayer == "data" && imports.any { ".presentation." in ".$it." }) {
                    add("$path: data imports presentation")
                }
                if (currentLayer == "domain" && imports.any {
                        it.contains(".data.") || it.contains(".presentation.")
                    }) {
                    add("$path: domain imports data or presentation")
                }
                if (currentLayer == "core" && imports.any { it.contains(".feature.") }) {
                    add("$path: core imports feature")
                }
                val hasComponentLogic = isAndroidComponent(source) &&
                    Regex("(?i)(repository|usecase)").containsMatchIn(source)
                if (hasComponentLogic) {
                    add("$path: Android component contains repository/use-case logic")
                }
                if (source.lineSequence().map(String::trim).filter { it.startsWith("typealias ") }
                        .any { Regex("(?i)\\b\\w*(dto|entity|domain)\\w*\\b").containsMatchIn(it) }) {
                    add("$path: DTO, Room entity, and domain model aliases are forbidden")
                }
                val featureNames = packageName.split(".").dropWhile { it != "feature" }.drop(1).take(1)
                val currentFeature = featureNames.firstOrNull()
                val crossFeatureImplementation = currentFeature != null && imports.any {
                    ".feature." in it && !it.contains(".feature.$currentFeature.")
                        && (".data." in it || ".presentation." in it)
                }
                if (crossFeatureImplementation) {
                    add("$path: feature imports another feature implementation")
                }
            }
        }

    private fun packageName(source: String): String =
        source.lineSequence()
            .firstOrNull { it.trim().startsWith("package ") }
            ?.trim()
            ?.removePrefix("package ")
            .orEmpty()

    private fun isAndroidComponent(source: String): Boolean =
        componentTypes.any { Regex(":\\s*\\w*$it\\b").containsMatchIn(source) }
}
