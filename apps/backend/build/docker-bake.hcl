group "default" {
  targets = ["api", "worker", "migrator"]
}

target "common" {
  context = "."
}

target "api" {
  inherits = ["common"]
  dockerfile = "apps/backend/build/Dockerfile.api"
  tags = ["indexshelf/api:dev"]
}

target "worker" {
  inherits = ["common"]
  dockerfile = "apps/backend/build/Dockerfile.worker"
  tags = ["indexshelf/worker:dev"]
}

target "migrator" {
  inherits = ["common"]
  dockerfile = "apps/backend/build/Dockerfile.migrator"
  tags = ["indexshelf/migrator:dev"]
}
