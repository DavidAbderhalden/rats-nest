"""Schema for the authentication model table"""
from datetime import datetime

from pydantic import Field

from .base_schema import BaseSchema

class AuthenticationsBase(BaseSchema):
    host_name: str = Field(examples=['127.0.0.1'])

class AuthenticationsCreate(AuthenticationsBase):
    customer_id: int = Field()
    auth_token: str = Field()

class AuthenticationsRead(AuthenticationsBase):
    issued_at_time: datetime = Field()
    id: int = Field()
