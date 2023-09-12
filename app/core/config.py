from os import environ

from pydantic import BaseSettings


class Settings(BaseSettings):
    ENV: str = "local"
    PATH_PREFIX: str = ""
    APP_HOST: str = "http://127.0.0.1"
    APP_PORT: int = 8080
    APP_TITLE: str = "fast_api_app"
    APP_DESCRIPTION: str = "Микросервис, реализующий "
    secret: str = "SECRET"

    DATABASE_URL: str = "sqlite+aiosqlite:///./app_db.sqlite"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


def get_settings() -> Settings:
    env = environ.get("ENV", "local")
    if env == "local":
        return Settings()
    return Settings()


settings = get_settings()
