"""Schema used to authenticate customers"""
from typing import Optional, Any

from pydantic import Field, model_validator

from .base_schema import BaseSchema
from .libs import Email


class IdentificationBase(BaseSchema):
    username: Optional[str] = Field(default=None, examples=['NekroQuest'], validate_default=True)
    email: Optional[Email] = Field(default=None, examples=['example@example.com'], validate_default=True)

    @model_validator(mode='after')
    def check_username_or_email(self) -> Any:
        email = self.email
        username = self.username
        if not email and not username:
            raise ValueError('either a username or email must be provided')
        return self


class IdentificationCreate(IdentificationBase):
    client_host: Optional[str] = Field(default=None)
    password: str = Field(examples=['kWd0$3#s@H93_'])

class IdentificationRead(IdentificationBase):
    # TODO: Add additional information
    pass
