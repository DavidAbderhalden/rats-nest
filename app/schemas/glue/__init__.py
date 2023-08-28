"""
Glue schemas are used to combine basic schemas with each other.
The basic pydantic schemas are modeled to represent SQLAlchemy models.
"""
from .post_register_request_schema import CustomersGlue, AddressGlue, StreetGlue
