from enum import StrEnum
from sqlalchemy import Column, ForeignKey, VARCHAR, INT, DATE, TIMESTAMP, func
from sqlalchemy.orm import relationship, Relationship
from app.services import databaseOperationsService
from app.utils import SQLStrEnum

# TODO: New version of modeling syntax
# TODO: Use the 'alembic' libs for data migration

class Roles(StrEnum):
    SUPER_ADMIN: str = 'super_admin'
    ADMIN: str = 'admin'
    SUPER_USER: str = 'super_user'
    USER: str = 'user'


class TestModel(databaseOperationsService.BaseModel):
    __tablename__: str = 'test'
    __allow_unmapped__ = True # TODO: Can be removed after refactoring

    id: Column = Column(INT, primary_key=True, index=True, autoincrement=True, unique=True, nullable=False)

class CustomersModel(databaseOperationsService.BaseModel):
    __tablename__: str = 'customers'
    __allow_unmapped__ = True # TODO: Can be removed after refactoring

    # columns
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

    # relationships
    lookup_customer_billings_relationship: Relationship = relationship(
        'LookupCustomerBillingsModel', back_populates='customers_relationship'
    )

    def __init__(self, **kwargs):
        super(CustomersModel, self).__init__(**kwargs)

class LookupCustomerBillingsModel(databaseOperationsService.BaseModel):
    __tablename__: str = 'lookup_customer_billings'
    __allow_unmapped__ = True # TODO: Can be removed after refactoring

    # columns
    customer_id: Column = Column(
        INT, ForeignKey('customers.customer_id'), primary_key=True, nullable=False, unique=False, index=True
    )
    billing_profile_id: Column = Column(
        INT, ForeignKey('billing_profiles.billing_profile_id'), primary_key=True, nullable=False, unique=False, index=True
    )
    priority: Column = Column(INT, nullable=False)

    # relationships
    customers_relationship: Relationship = relationship(
        'CustomersModel', back_populates='lookup_customer_billings_relationship'
    )
    billing_profiles_relationship: Relationship = relationship(
        'BillingProfilesModel', back_populates='lookup_customer_billings_relationship'
    )

    def __init__(self, **kwargs):
        super(LookupCustomerBillingsModel, self).__init__(**kwargs)


class BillingProfilesModel(databaseOperationsService.BaseModel):
    __tablename__ = 'billing_profiles'
    __allow_unmapped__ = True # TODO: Can be removed after refactoring

    # columns
    billing_profile_id: Column = Column(INT, primary_key=True, index=True, autoincrement=True, unique=True, nullable=False)
    card_number: Column = Column(INT, nullable=False)
    card_name: Column = Column(VARCHAR(45), nullable=False)
    expiry_date: Column = Column(DATE, nullable=False)
    cvv: Column = Column(INT, nullable=False)

    # relationships
    lookup_customer_billings_relationship: Relationship = relationship(
        'LookupCustomerBillingsModel', back_populates='billing_profiles_relationship'
    )

    def __init__(self, **kwargs):
        super(BillingProfilesModel, self).__init__(**kwargs)