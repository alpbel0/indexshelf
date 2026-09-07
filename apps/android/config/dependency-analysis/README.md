# Android dependency analysis

The package architecture tests enforce dependency direction before feature implementations
exist: presentation cannot import data, data cannot import presentation, domain cannot import
data or presentation, core cannot import features, Android components cannot contain repository
or use-case dependencies, and DTO/Room-entity/domain-model aliases are forbidden.

Run from `apps/android` with `./gradlew test detekt spotlessCheck`.
