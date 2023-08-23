"""The sqlalchemy model for orders table"""
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship, mapped_column, Mapped

from .base_model import BaseModel

if TYPE_CHECKING:
    from .customers_model import CustomersModel
    from .lookup_order_products_model import LookupOrderProductsModel


class OrdersModel(BaseModel):
    # primary keys
    order_id: Mapped[int] = \
        mapped_column(Integer, primary_key=True, unique=True, autoincrement=True, index=True)

    additional_information: Mapped[str] = mapped_column(String(128), nullable=True)
    order_time: Mapped[int] = mapped_column(Integer, insert_default=func.current_timestamp())

    # foreign keys
    customer_id: Mapped[int] = mapped_column(Integer, ForeignKey('customers.customer_id'))

    # relationships
    order_customer_relationship: Mapped['CustomersModel'] = \
        relationship(back_populates='customer_order_relationship')
    order_lookup_order_product_relationship: Mapped['LookupOrderProductsModel'] = \
        relationship(back_populates='lookup_order_product_order_relationship')
