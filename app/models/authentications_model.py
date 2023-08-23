"""The sqlalchemy model for authentications table"""
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship, mapped_column, Mapped

from .base_model import BaseModel

if TYPE_CHECKING:
    from .customers_model import CustomersModel


class AuthenticationsModel(BaseModel):
    # primary keys
    authentication_id: Mapped[int] = \
        mapped_column(Integer, primary_key=True, unique=True, autoincrement=True, index=True)

    issued_at_time: Mapped[int] = mapped_column(Integer, insert_default=func.current_timestamp())
    host_name: Mapped[str] = mapped_column(String(45))
    ip_address: Mapped[str] = mapped_column(String(15))

    # foreign keys
    customer_id: Mapped[int] = mapped_column(Integer, ForeignKey('customers.customer_id'))

    # relationships
    authentication_customer_relationship: Mapped['CustomersModel'] = \
        relationship(back_populates='customer_authentication_relationship')
