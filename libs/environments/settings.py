from pydantic import Field
from functools import lru_cache
from pydantic_settings import BaseSettings

class Base(BaseSettings):
    DATABASE_USER: str | None = Field('database_username', env='DATABASE_USER')
    DATABASE_PASSWORD: str | None = Field('database_password', env='DATABASE_PASSWORD')
    DATABASE_HOST: str | None = Field('database_host', env='DATABASE_HOST')
    DATABASE_PORT: int | None = Field(3306, env='DATABASE_PORT')
    DATABASE_NAME: str | None = Field('database_name', env='DATABASE_NAME')

@lru_cache
def get_app_settings() -> Base:
    return Base()