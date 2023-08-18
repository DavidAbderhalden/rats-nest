from enum import StrEnum
from sqlalchemy import Column, VARCHAR, INT, DATE, TIMESTAMP, func
from sqlalchemy.orm import relationship, Relationship
from libs.services.database_operations import DatabaseOperationsService
from libs.utils.database_util import SQLStrEnum


class Roles(StrEnum):
    SUPER_ADMIN: str = 'super_admin'
    ADMIN: str = 'admin'
    SUPER_USER: str = 'super_user'
    USER: str = 'user'


class CustomersModel(DatabaseOperationsService.Base):
    __tablename__: str = 'customers'

    customer_id: Column = Column(INT, primary_key=True, index=True, autoincrement=True, unique=True, nullable=False)
    username: Column = Column(VARCHAR(45), nullable=False, unique=True, index=True)
    primary_email: Column = Column(VARCHAR(45), nullable=False, unique=True, index=True)
    secondary_email: Column = Column(VARCHAR(45), nullable=True, unique=False)
    password: Column = Column(VARCHAR(100), nullable=False)
    first_name: Column = Column(VARCHAR(45), nullable=False)
    last_name: Column = Column(VARCHAR(45), nullable=False)
    phone_number: Column = Column(VARCHAR(45), nullable=True, unique=True)
    birthdate: Column = Column(DATE, nullable=False)
    role: Column = Column(SQLStrEnum(Roles), nullable=False, server_default=Roles.USER)
    registration_date: Column = Column(TIMESTAMP, nullable=False, server_default=func.current_timestamp())

    lookup_customer_billings_relationship: Relationship = relationship(
        'LookupCustomerBillings', back_populates='customers.customer_id'
    )
