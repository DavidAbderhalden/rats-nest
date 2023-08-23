"""The sqlalchemy model for cities table"""
from typing import TYPE_CHECKING

from sqlalchemy import Integer, String, Enum
from sqlalchemy.orm import relationship, mapped_column, Mapped

from .base_model import BaseModel
from .enums import Countries

if TYPE_CHECKING:
    from .streets_model import StreetsModel


class CitiesModel(BaseModel):
    # primary keys
    city_id: Mapped[int] = \
        mapped_column(Integer, primary_key=True, unique=True, autoincrement=True, index=True)

    zip_code: Mapped[int] = mapped_column(Integer, unique=True, index=True)
    name: Mapped[str] = mapped_column(String(45))

    # enums
    country: Mapped[Countries] = mapped_column(Enum(Countries))

    # relationships
    city_street_relationship: Mapped['StreetsModel'] = \
        relationship(back_populates='street_city_relationship')
