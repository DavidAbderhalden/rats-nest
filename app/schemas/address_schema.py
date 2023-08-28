"""Address schema"""
from pydantic import ConfigDict, Field

from .base_schema import BaseSchema

class AddressBase(BaseSchema):
    model_config = ConfigDict(title='Address', from_attributes=True, extra='ignore')
    house_number: str = Field(examples=['81a'])

class AddressCreate(AddressBase):
    street_id: int

class AddressRead(AddressBase):
    id: int = Field()
