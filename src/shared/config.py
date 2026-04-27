from datetime import timedelta

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel
from typing import ClassVar, Literal
from pathlib import Path
import logging

BASE_DIR = Path(__file__).resolve().parent.parent.parent
LOG_DEFAULT_FORMAT = (
    "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"
)


class MiddlewareConfig(BaseModel):
    cors_allowed_origins: list[str] = [
        "http://localhost",
        "http://localhost:5173",
    ]


class SQLAlchemyConfig(BaseSettings):
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 10
    max_overflow: int = 10


class PostgresConfig(BaseModel):
    naming_convention: ClassVar[dict] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }

    user: str
    password: str
    host: str
    port: int
    db: str
    alchemy_config: SQLAlchemyConfig = SQLAlchemyConfig()

    @property
    def dsn(self) -> str:
        return (
            f"postgresql+asyncpg://{self.user}:{self.password}@"
            f"{self.host}:{self.port}/{self.db}"
        )


class RedisConfig(BaseModel):
    host: str
    port: int
    db: str

    @property
    def dsn(self) -> str:
        return f"redis://{self.host}:{self.port}/{self.db}"


class JWTConfig(BaseModel):
    secret_key: str
    algorithm: str = "HS256"
    expire_timedelta: timedelta = timedelta(days=10)


class LoggingConfig(BaseModel):
    log_level: Literal[
        "debug",
        "info",
        "warning",
        "error",
        "critical",
    ] = "info"

    log_format: str = LOG_DEFAULT_FORMAT

    @property
    def log_level_value(self) -> int:
        return logging.getLevelNamesMapping()[self.log_level.upper()]


class PrefixConfig(BaseModel):
    api_v1: str = "/api/v1"
    landings: str = "/landings"
    core: str = "/core"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(BASE_DIR / ".env",),
        env_prefix="APP_CONFIG__",
        env_nested_delimiter="__",
        case_sensitive=False,
    )

    db: PostgresConfig
    redis: RedisConfig
    midd: MiddlewareConfig
    jwt: JWTConfig
    logging: LoggingConfig = LoggingConfig()
    prefix: PrefixConfig = PrefixConfig()


settings = Settings()
