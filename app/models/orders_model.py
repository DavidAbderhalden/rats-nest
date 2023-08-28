"""The sqlalchemy model for orders table"""
from typing import TYPE_CHECKING

from datetime import datetime

from sqlalchemy import ForeignKey, Integer, String, func, DateTime
from sqlalchemy.orm import relationship, mapped_column, Mapped

from .base_model import BaseModel

if TYPE_CHECKING:
    from .customers_model import CustomersModel
    from .lookup_order_products_model import LookupOrderProductsModel


class OrdersModel(BaseModel):
    # primary keys
    id: Mapped[int] = \
        mapped_column(Integer, primary_key=True, unique=True, autoincrement=True, index=True)

    additional_information: Mapped[str] = mapped_column(String(128), nullable=True)
    order_time: Mapped[datetime] = mapped_column(DateTime, insert_default=func.now())

    # foreign keys
    customer_id: Mapped[int] = mapped_column(Integer, ForeignKey('customers.id', ondelete='CASCADE'))

    # relationships
    order_customer_relationship: Mapped['CustomersModel'] = \
        relationship(back_populates='customer_order_relationship')
    order_lookup_order_product_relationship: Mapped['LookupOrderProductsModel'] = \
        relationship(back_populates='lookup_order_product_order_relationship')
