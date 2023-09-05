"""Streets schema"""
from pydantic import ConfigDict, Field

from .base_schema import BaseSchema

class StreetsBase(BaseSchema):
    model_config = ConfigDict(title='Streets', from_attributes=True, extra='ignore')
    name: str = Field(examples=['Hauptstrasse'])

class StreetsCreate(StreetsBase):
    city_id: int = Field()

class StreetsRead(StreetsBase):
    city_id: int = Field()
    id: int = Field()
