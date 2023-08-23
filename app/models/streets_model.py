"""The sqlalchemy model for streets table"""
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import relationship, mapped_column, Mapped

from .base_model import BaseModel

if TYPE_CHECKING:
    from .cities_model import CitiesModel
    from .address_model import AddressModel


class StreetsModel(BaseModel):
    # primary keys
    street_id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True, autoincrement=True, index=True)

    name: Mapped[str] = mapped_column(String(45))

    # foreign keys
    city_id: Mapped[int] = mapped_column(Integer, ForeignKey('cities.city_id'))

    # relationships
    street_city_relationship: Mapped['CitiesModel'] = \
        relationship(back_populates='city_street_relationship')
    street_address_relationship: Mapped['AddressModel'] = \
        relationship(back_populates='address_street_relationship')
