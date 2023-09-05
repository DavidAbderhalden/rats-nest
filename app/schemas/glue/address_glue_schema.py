"""Address glue pydantic schemas"""
from pydantic import Field

from ..address_schema import AddressBase
from .streets_glue_schema import StreetsGlueBase


class AddressGlueBase(AddressBase):
    street: StreetsGlueBase = Field()

class AddressGlueCreate(AddressGlueBase):
    pass

class AddressGlueRead(AddressGlueBase):
    id: int = Field()
