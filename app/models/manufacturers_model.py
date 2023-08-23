"""The sqlalchemy model for manufacturers table"""
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import relationship, mapped_column, Mapped

from .base_model import BaseModel

if TYPE_CHECKING:
    from .address_model import AddressModel
    from .products_model import ProductsModel


class ManufacturersModel(BaseModel):
    # primary keys
    manufacturer_id: Mapped[int] = \
        mapped_column(Integer, primary_key=True, unique=True, autoincrement=True, index=True)

    name: Mapped[str] = mapped_column(String(45))
    contact_email: Mapped[str] = mapped_column(String(45), nullable=True)

    # foreign keys
    headquarter_address_id: Mapped[int] = mapped_column(Integer, ForeignKey('address.address_id'))

    # relationships
    manufacturer_address_relationship: Mapped['AddressModel'] = \
        relationship(back_populates='address_manufacturer_relationship')
    manufacturer_product_relationship: Mapped['ProductsModel'] = \
        relationship(back_populates='product_manufacturer_relationship')
