plugins {
    id("io.gitlab.arturbosch.detekt")
    id("com.diffplug.spotless")
}

detekt {
    config.setFrom(files("$rootDir/config/detekt/detekt.yml"))
    buildUponDefaultConfig = true
    autoCorrect = false
}

spotless {
    kotlin {
        target("**/*.kt")
        trimTrailingWhitespace()
        endWithNewline()
    }
}

tasks.withType<Test>().configureEach {
    useJUnit()
}
