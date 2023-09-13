"""Application settings, loaded from environment variables"""
from os import path

from typing import AnyStr

from pydantic import Field
from pydantic_settings import BaseSettings


def path_to(struct: list[str]) -> AnyStr:
    project_root: str = path.join(path.dirname(__file__), '..')
    return path.abspath(path.join(project_root, *struct))

class Settings(BaseSettings):
    DATABASE_USER: str = Field('database_username', env='DATABASE_USER')
    DATABASE_PASSWORD: str = Field('database_password', env='DATABASE_PASSWORD')
    DATABASE_HOST: str = Field('database_host', env='DATABASE_HOST')
    DATABASE_PORT: int = Field(3306, env='DATABASE_PORT')
    DATABASE_NAME: str = Field('database_name', env='DATABASE_NAME')
    ENVIRONMENT: str = Field('production', env='ENVIRONMENT')
    MAIL_USERNAME: str = Field('email_username', env='MAIL_USERNAME')
    MAIL_PASSWORD: str = Field('email_password', env='MAIL_PASSWORD')
    MAIL_FROM: str = Field('example@example.com', env='MAIL_FROM')
    MAIL_PORT: int = Field(587, env='MAIL_PORT')
    MAIL_SERVER: str = Field('email_server', env='MAIL_SERVER')
    MAIL_FROM_NAME: str = Field('Example', env='MAIL_FROM_NAME')
    MAIL_TEMPLATE_PATH: str = Field(path_to(['templates', 'email']))
    MAIL_IMAGE_PATH: str = Field(path_to(['templates', 'email', 'images']))
    MAIL_STARTTLS: bool = Field('no', env='MAIL_STARTTLS')
    MAIL_SSL_TLS: bool = Field('yes', env='MAIL_SSL_TLS')
    MAIL_USE_CREDENTIALS: bool = Field('yes', env='MAIL_USE_CREDENTIALS')
    MAIL_VALIDATE_CERTS: bool = Field('yes', env='MAIL_VALIDATE_CERTS')
    RATS_NEST_DOMAIN: str = Field('localhost:8000', env='RATS_NEST_DOMAIN')
    JWT_SECRET_KEY: str = Field('secret_key', env='JWT_SECRET_KEY')


settings = Settings()
