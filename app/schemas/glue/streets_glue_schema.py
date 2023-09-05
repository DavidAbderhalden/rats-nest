"""Streets glue pydantic schemas"""
from pydantic import Field

from ..streets_schema import StreetsBase
from ..cities_schema import CitiesBase


class StreetsGlueBase(StreetsBase):
    city: CitiesBase = Field()

class StreetsGlueCreate(StreetsGlueBase):
    pass

class StreetsGlueRead(StreetsGlueBase):
    id: int = Field()
