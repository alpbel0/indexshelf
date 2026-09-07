import os
from dataclasses import dataclass


@dataclass(frozen=True)
class WorkerProfile:
    name: str
    enabled: bool = True


DEFAULT_WORKER_PROFILE = WorkerProfile(name="bootstrap")

SUPPORTED_WORKER_PROFILES = frozenset({"metadata", "static", "media", "outbox"})


def profile_from_environment() -> WorkerProfile:
    name = os.getenv("INDEXSHELF_DATA_WORKER_PROFILE", DEFAULT_WORKER_PROFILE.name)
    if name == DEFAULT_WORKER_PROFILE.name:
        return DEFAULT_WORKER_PROFILE
    if name not in SUPPORTED_WORKER_PROFILES:
        raise ValueError(f"Unsupported worker profile: {name}")
    return WorkerProfile(name=name)
