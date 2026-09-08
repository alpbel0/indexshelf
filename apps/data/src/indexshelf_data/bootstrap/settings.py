from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class DataSettings(BaseSettings):
    environment: str = "local"
    log_level: str = "INFO"
    health_host: str = "127.0.0.1"
    health_port: int = 8081
    secret_reference: str | None = None
    database_url: str = "postgresql+asyncpg://indexshelf_data_runtime:indexshelf_data_runtime_dummy@localhost:55433/indexshelf_data"
    alembic_database_url: str = "postgresql+psycopg://indexshelf_data_migrator:indexshelf_data_migrator_dummy@localhost:55433/indexshelf_data"
    rabbitmq_url: str = "amqp://indexshelf_data:data_dummy_password@localhost:55673/%2Findexshelf"
    model_config = SettingsConfigDict(env_prefix="INDEXSHELF_DATA_", extra="ignore")

    @model_validator(mode="after")
    def validate_secret_reference(self) -> "DataSettings":
        if self.environment not in {"local", "staging", "production"}:
            raise ValueError("environment must be local, staging, or production")
        if self.environment in {"staging", "production"} and self.secret_reference is None:
            raise ValueError("secret_reference is required outside local environment")
        if self.secret_reference is not None:
            from pathlib import Path

            if not Path(self.secret_reference).is_file():
                raise ValueError("secret_reference must point to an existing file")
        return self
