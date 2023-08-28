"""Cities schema"""
from pydantic import ConfigDict, Field

from app.models import Countries

from .base_schema import BaseSchema

class CitiesBase(BaseSchema):
    model_config = ConfigDict(title='Cities', from_attributes=True, extra='ignore')
    zip_code: int = Field(examples=[8000], ge=1000, le=10000)
    name: str = Field(examples=['Zürich'])
    country: Countries = Field(examples=[Countries.CH])

CitiesCreate = CitiesBase

class CitiesRead(CitiesBase):
    id: int = Field()
