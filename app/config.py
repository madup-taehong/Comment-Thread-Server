import os

from pydantic import BaseModel, BaseSettings


class DBConnection(BaseModel):
    SQLALCHEMY_DATABASE_URL: str = ""


class Settings(BaseSettings):
    API_VERSION: str = "/v1"

    DB_INFOS: DBConnection = DBConnection(
        SQLALCHEMY_DATABASE_URL="postgresql://postgres:postgres@localhost:5432/comment_thread_db"
    )
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/comment_thread_db"

    SECRET_KEY: str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30


class TestSettings(Settings):
    DB_INFOS = DBConnection(SQLALCHEMY_DATABASE_URL="postgresql://test_user:test_password@localhost:5433/test_db")
    DATABASE_URL = "postgresql://test_user:test_password@localhost:5433/test_db"


def get_settings():
    server_env = os.environ.get("FASTAPI_ENV")
    if server_env == "dev":
        return Settings()
    return TestSettings()


settings = get_settings()
