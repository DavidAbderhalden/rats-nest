"""The sqlalchemy model for customers table"""
from typing import Optional, TYPE_CHECKING
from datetime import date, datetime

from sqlalchemy import ForeignKey, Integer, String, Enum, func, DateTime
from sqlalchemy.orm import relationship, mapped_column, Mapped

from .base_model import BaseModel
from .enums import Roles

if TYPE_CHECKING:
    from .billing_profiles_model import BillingProfilesModel
    from .authentications_model import AuthenticationsModel
    from .orders_model import OrdersModel
    from .address_model import AddressModel


class CustomersModel(BaseModel):
    # primary keys
    id: Mapped[int] = mapped_column(primary_key=True, unique=True, autoincrement=True, index=True)

    username: Mapped[str] = mapped_column(String(20), unique=True, index=True)
    primary_email: Mapped[str] = mapped_column(String(45), unique=True, index=True)
    secondary_email: Mapped[Optional[str]] = mapped_column(String(45), nullable=True)
    password: Mapped[str] = mapped_column(String(100))
    first_name: Mapped[str] = mapped_column(String(20))
    last_name: Mapped[str] = mapped_column(String(20))
    phone_number: Mapped[Optional[str]] = mapped_column(String(15), nullable=True)
    birthdate: Mapped[date] = mapped_column(String(10))
    registration_time: Mapped[datetime] = mapped_column(DateTime, insert_default=func.now())

    # enums
    role: Mapped[Roles] = mapped_column(Enum(Roles), insert_default=Roles.USER)

    # foreign keys
    delivery_address_id: Mapped[int] = mapped_column(Integer, ForeignKey('address.id', ondelete='RESTRICT'))
    home_address_id: Mapped[int] = mapped_column(Integer, ForeignKey('address.id', ondelete='RESTRICT'))

    # relationships
    customer_billing_profile_relationship: Mapped['BillingProfilesModel'] = \
        relationship(back_populates='billing_profile_customer_relationship')
    customer_authentication_relationship: Mapped['AuthenticationsModel'] = \
        relationship(back_populates='authentication_customer_relationship')
    customer_order_relationship: Mapped['OrdersModel'] = \
        relationship(back_populates='order_customer_relationship')
    customer_confirmation_codes_relationship: Mapped['ConfirmationCodesModel'] = \
        relationship(back_populates='confirmation_codes_customer_relationship')
    customer_delivery_address_relationship: Mapped['AddressModel'] = \
        relationship(back_populates='delivery_address_customer_relationship', foreign_keys=[delivery_address_id])
    customer_home_address_relationship: Mapped['AddressModel'] = \
        relationship(back_populates='home_address_customer_relationship', foreign_keys=[home_address_id])
