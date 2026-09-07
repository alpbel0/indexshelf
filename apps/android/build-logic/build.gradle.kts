plugins {
    `kotlin-dsl`
}

repositories {
    google()
    mavenCentral()
    gradlePluginPortal()
}

dependencies {
    implementation("com.android.tools.build:gradle:8.7.3")
    implementation("org.jetbrains.kotlin:kotlin-gradle-plugin:2.4.10")
    implementation("org.jetbrains.kotlin:compose-compiler-gradle-plugin:2.4.10")
    implementation("com.google.dagger:hilt-android-gradle-plugin:2.52")
    implementation("io.gitlab.arturbosch.detekt:detekt-gradle-plugin:1.23.8")
    implementation("com.diffplug.spotless:spotless-plugin-gradle:7.0.2")
}
