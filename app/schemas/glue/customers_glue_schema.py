"""Customers glue pydantic schemas"""
from pydantic import Field

from ..customers_schema import CustomersBase
from .address_glue_schema import AddressGlueCreate


class CustomersGlueBase(CustomersBase):
    delivery_address: AddressGlueCreate = Field()
    home_address: AddressGlueCreate = Field()

class CustomersGlueCreate(CustomersGlueBase):
    password: str = Field(max_length=100, examples=['kWd0$3#s@H93_'])

class CustomersGlueRead(CustomersGlueBase):
    id: int = Field()
