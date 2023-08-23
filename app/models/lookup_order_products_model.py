"""The sqlalchemy model for lookup order products table"""
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import relationship, mapped_column, Mapped

from .base_model import BaseModel

if TYPE_CHECKING:
    from .orders_model import OrdersModel
    from .products_model import ProductsModel


class LookupOrderProductsModel(BaseModel):
    # primary keys / foreign keys
    order_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('orders.order_id'), primary_key=True, unique=False, autoincrement=False, index=True
    )
    product_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('products.product_id'), primary_key=True, unique=False, autoincrement=False, index=True
    )

    quantity: Mapped[int] = mapped_column(Integer)

    # relationships
    lookup_order_product_order_relationship: Mapped['OrdersModel'] = \
        relationship(back_populates='order_lookup_order_product_relationship')
    lookup_order_product_product_relationship: Mapped['ProductsModel'] = \
        relationship(back_populates='product_lookup_order_product_relationship')
