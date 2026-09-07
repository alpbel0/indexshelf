plugins {
    id("org.jetbrains.kotlin.plugin.compose")
}

dependencies {
    add("implementation", platform("androidx.compose:compose-bom:2024.12.01"))
    add("implementation", "androidx.compose.ui:ui")
    add("implementation", "androidx.compose.ui:ui-tooling-preview")
    add("implementation", "androidx.compose.material3:material3")
}
