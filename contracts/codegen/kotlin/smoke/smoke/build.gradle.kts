plugins { kotlin("jvm") }

dependencies {
    implementation(kotlin("stdlib"))
    implementation("com.google.code.gson:gson:2.12.1")
}

sourceSets.main { java.srcDir("../../../../generated/kotlin/src/main/kotlin") }

kotlin { jvmToolchain(21) }
