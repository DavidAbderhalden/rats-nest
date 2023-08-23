"""The sqlalchemy model for address table"""
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import relationship, mapped_column, Mapped

from .base_model import BaseModel

if TYPE_CHECKING:
    from .streets_model import StreetsModel
    from .manufacturers_model import ManufacturersModel
    from .customers_model import CustomersModel


class AddressModel(BaseModel):
    # primary keys
    address_id: Mapped[int] = \
        mapped_column(Integer, primary_key=True, unique=True, autoincrement=True, index=True)

    house_number: Mapped[str] = mapped_column(String(5))

    # foreign keys
    street_id: Mapped[int] = mapped_column(Integer, ForeignKey('streets.street_id'))

    # relationships
    address_street_relationship: Mapped['StreetsModel'] = \
        relationship(back_populates="street_address_relationship")
    address_manufacturer_relationship: Mapped['ManufacturersModel'] = \
        relationship(back_populates='manufacturer_address_relationship')
    delivery_address_customer_relationship: Mapped['CustomersModel'] = \
        relationship(
            back_populates='customer_delivery_address_relationship',
            foreign_keys='CustomersModel.delivery_address_id'
        )
    home_address_customer_relationship: Mapped['CustomersModel'] = \
        relationship(
            back_populates='customer_home_address_relationship',
            foreign_keys='CustomersModel.home_address_id'
        )
