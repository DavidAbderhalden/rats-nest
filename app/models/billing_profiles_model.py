"""The sqlalchemy model for billing profiles table"""
from typing import TYPE_CHECKING

from datetime import date

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import relationship, mapped_column, Mapped

from .base_model import BaseModel

if TYPE_CHECKING:
    from .customers_model import CustomersModel


class BillingProfilesModel(BaseModel):
    # primary keys
    billing_profile_id: Mapped[id] = \
        mapped_column(Integer, primary_key=True, unique=True, autoincrement=True, index=True)

    card_number: Mapped[int] = mapped_column(Integer)
    card_name: Mapped[str] = mapped_column(String(20))
    expiry_date: Mapped[date] = mapped_column(String(10))
    cvv: Mapped[int] = mapped_column(Integer)
    priority: Mapped[int] = mapped_column(Integer)

    # foreign keys
    customer_id: Mapped[int] = mapped_column(Integer, ForeignKey('customers.customer_id'))

    # relationships
    billing_profile_customer_relationship: Mapped['CustomersModel'] = \
        relationship(back_populates='customer_billing_profile_relationship')
