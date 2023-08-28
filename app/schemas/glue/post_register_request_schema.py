"""Glue schemas for register account endpoint"""
from pydantic import Field

from ..customers_schema import CustomersBase
from ..address_schema import AddressBase
from ..streets_schema import StreetsBase
from ..cities_schema import CitiesBase

class StreetGlue(StreetsBase):
    city: CitiesBase = Field()

class AddressGlue(AddressBase):
    street: StreetGlue = Field()

class CustomersGlue(CustomersBase):
    password: str = Field(max_length=100, examples=['kWd0$3#s@H93_'])
    delivery_address: AddressGlue = Field()
    home_address: AddressGlue = Field()
