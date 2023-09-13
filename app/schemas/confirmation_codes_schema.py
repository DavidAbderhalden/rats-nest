"""Confirmation Codes schema"""
from typing import Optional

from pydantic import ConfigDict, Field

from .base_schema import BaseSchema

class ConfirmationCodesBase(BaseSchema):
    model_config = ConfigDict(title='Customers', from_attributes=True, extra='ignore')
    email_validation: Optional[str] = Field(max_length=30, default=None)
    password_reset: Optional[str] = Field(max_length=30, default=None)

class ConfirmationCodesCreate(ConfirmationCodesBase):
    customer_id: int = Field()

class ConfirmationCodesUpdate(ConfirmationCodesBase):
    pass

class ConfirmationCodesRead(ConfirmationCodesBase):
    id: int = Field()
