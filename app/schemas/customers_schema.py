"""Customers schema"""
from datetime import datetime

from typing import Optional

from pydantic import ConfigDict, Field

from app.models import Roles

from .libs import Email, CustomDate
from .base_schema import BaseSchema


class CustomersBase(BaseSchema):
    model_config = ConfigDict(title='Customers', from_attributes=True, extra='ignore')
    username: str = Field(max_length=20, examples=['NekroQuest'])
    primary_email: Email = Field(max_length=45, examples=['example@example.com'])
    secondary_email: Optional[Email] = Field(default=None, max_length=45, examples=['example@example.com'])
    first_name: str = Field(max_length=20, examples=['Joshua'])
    last_name: str = Field(max_length=20, examples=['Taylor'])
    phone_number: Optional[str] = Field(default=None, max_length=15, examples=['+41791112132'])
    birthdate: CustomDate = Field(max_length=10, examples=['18.04.2004'])


class CustomersCreate(CustomersBase):
    password: str = Field(max_length=100, examples=['kWd0$3#s@H93_'])
    delivery_address_id: int = Field()
    home_address_id: int = Field()


class CustomersRead(CustomersBase):
    delivery_address_id: int = Field()
    home_address_id: int = Field()
    role: Roles = Field(examples=[Roles.USER])
    registration_time: datetime = Field(examples=[datetime.now()])
