"""
Glue schemas are used to combine basic schemas with each other.
The basic pydantic schemas are modeled to represent SQLAlchemy models.
"""
from .customers_glue_schema import CustomersGlueCreate, CustomersGlueRead
from .address_glue_schema import AddressGlueCreate, AddressGlueRead
from .streets_glue_schema import StreetsGlueCreate, StreetsGlueRead
