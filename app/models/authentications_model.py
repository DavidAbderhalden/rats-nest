"""The sqlalchemy model for authentications table"""
from typing import TYPE_CHECKING

from datetime import datetime

from sqlalchemy import ForeignKey, Integer, String, func, DateTime
from sqlalchemy.orm import relationship, mapped_column, Mapped

from .base_model import BaseModel

if TYPE_CHECKING:
    from .customers_model import CustomersModel


class AuthenticationsModel(BaseModel):
    # primary keys
    # TODO: Should be unique token instead of integer
    id: Mapped[int] = \
        mapped_column(Integer, primary_key=True, unique=True, autoincrement=True, index=True)

    # 36 is max length of uuid (32x characters 4x "-")
    auth_token: Mapped[str] = mapped_column(String(36), unique=True, nullable=False)
    issued_at_time: Mapped[datetime] = mapped_column(DateTime, insert_default=func.now())
    host_name: Mapped[str] = mapped_column(String(45))

    # foreign keys
    customer_id: Mapped[int] = mapped_column(Integer, ForeignKey('customers.id', ondelete='CASCADE'))

    # relationships
    authentication_customer_relationship: Mapped['CustomersModel'] = \
        relationship(back_populates='customer_authentication_relationship')
