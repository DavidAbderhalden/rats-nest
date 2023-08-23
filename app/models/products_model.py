"""The sqlalchemy model for products table"""
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String, Boolean, Float, JSON
from sqlalchemy.orm import relationship, mapped_column, Mapped

from .base_model import BaseModel
from .enums import ProductCategories

if TYPE_CHECKING:
    from .manufacturers_model import ManufacturersModel
    from .lookup_order_products_model import LookupOrderProductsModel


class ProductsModel(BaseModel):
    # primary keys
    product_id: Mapped[int] = \
        mapped_column(Integer, primary_key=True, unique=True, autoincrement=True, index=True)

    in_stock: Mapped[bool] = mapped_column(Boolean, insert_default=False)
    upc: Mapped[int] = mapped_column(Integer)
    price: Mapped[float] = mapped_column(Float)
    description: Mapped[str] = mapped_column(String(256), nullable=True)
    categories: Mapped[list[ProductCategories]] = mapped_column(JSON)

    # foreign keys
    manufacturer_id: Mapped[int] = mapped_column(Integer, ForeignKey('manufacturers.manufacturer_id'))

    # relationships
    product_manufacturer_relationship: Mapped['ManufacturersModel'] = \
        relationship(back_populates='manufacturer_product_relationship')
    product_lookup_order_product_relationship: Mapped['LookupOrderProductsModel'] = \
        relationship(back_populates='lookup_order_product_product_relationship')
