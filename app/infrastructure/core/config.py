from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    # Base de datos
    DATABASE_URL: str

    # Aplicación
    APP_NAME: str = "API Usuarios y Roles"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    CORS_ORIGINS: list[str] = ["http://localhost:5173", "http://localhost:3000"]

    # JWT
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_MINUTES: int = 15

    # Cache de estado del usuario autenticado (patrón híbrido)
    AUTH_CACHE_TTL_SEGUNDOS: int = 60
    AUTH_CACHE_MAX_ITEMS: int = 1000

    class Config:
        env_file = ".env"  # ← lee del archivo .env
        env_file_encoding = "utf-8"


@lru_cache  # ← crea la configuración una sola vez
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
