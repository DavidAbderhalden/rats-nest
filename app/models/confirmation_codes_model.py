"""The sqlalchemy model for confirmation codes table"""
from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey

from .base_model import BaseModel

if TYPE_CHECKING:
    from .customers_model import CustomersModel

class ConfirmationCodesModel(BaseModel):
    # primary keys
    id: Mapped[int] = mapped_column(primary_key=True, unique=True, autoincrement=True, index=True)

    email_validation: Mapped[str] = mapped_column(String(20), nullable=True, unique=True)
    password_reset: Mapped[str] = mapped_column(String(20), nullable=True, unique=True)

    # foreign keys
    customer_id: Mapped[int] = mapped_column(Integer, ForeignKey('customers.id', ondelete='CASCADE'))

    # relationships
    confirmation_codes_customer_relationship: Mapped['CustomersModel'] = \
        relationship(back_populates='customer_confirmation_codes_relationship')
