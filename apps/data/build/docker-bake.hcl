group "default" {
  targets = ["worker", "browser-headless", "browser-headful", "media", "migrator"]
}
target "worker" {
  context = "."
  dockerfile = "apps/data/build/Dockerfile.worker"
  tags = ["indexshelf/data-worker:dev"]
}
target "browser-headless" {
  context = "."
  dockerfile = "apps/data/build/Dockerfile.browser-headless"
  tags = ["indexshelf/data-browser-headless:dev"]
}
target "browser-headful" {
  context = "."
  dockerfile = "apps/data/build/Dockerfile.browser-headful"
  tags = ["indexshelf/data-browser-headful:dev"]
}
target "media" {
  context = "."
  dockerfile = "apps/data/build/Dockerfile.media"
  tags = ["indexshelf/data-media:dev"]
}
target "migrator" {
  context = "."
  dockerfile = "apps/data/build/Dockerfile.migrator"
  tags = ["indexshelf/data-migrator:dev"]
}
