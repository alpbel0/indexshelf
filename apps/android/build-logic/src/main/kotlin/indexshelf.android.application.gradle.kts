plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
    id("org.jetbrains.kotlin.kapt")
    id("com.google.dagger.hilt.android")
    id("indexshelf.android.quality")
}

android {
    namespace = "com.indexshelf.app"
    compileSdk = 35

    defaultConfig {
        applicationId = "com.indexshelf.app"
        minSdk = 26
        targetSdk = 35
        versionCode = 1
        versionName = "0.1.0"
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_21
        targetCompatibility = JavaVersion.VERSION_21
    }

    lint {
        checkTestSources = false
    }
}

kotlin {
    jvmToolchain(21)
}
