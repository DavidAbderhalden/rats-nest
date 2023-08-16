from pydantic import Field

from pydantic_settings import BaseSettings

class Base(BaseSettings):
    RANDOM_URL: str | None = Field('random_url', env='RANDOM_URL')

# TODO: Maybe classes for different envs