from enum import StrEnum
from typing import Optional
from sqlalchemy import ForeignKey, Integer, String, Enum, func
from sqlalchemy.orm import relationship, DeclarativeBase, declared_attr, mapped_column, Mapped
from app.utils import pascal_to_snake_case
from datetime import date


class BaseModel(DeclarativeBase):
    @declared_attr
    def __tablename__(self) -> str:
        tableName: str = self.__name__.split('Model', 1)[0]
        return pascal_to_snake_case(tableName)


class Roles(StrEnum):
    SUPER_ADMIN: str = 'super_admin'
    ADMIN: str = 'admin'
    SUPER_USER: str = 'super_user'
    USER: str = 'user'


class TestModel(BaseModel):
    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)


class CustomersModel(BaseModel):
    customer_id: Mapped[int] = mapped_column(primary_key=True, unique=True, autoincrement=True, index=True)
    username: Mapped[str] = mapped_column(String(20), unique=True, index=True)
    primary_email: Mapped[str] = mapped_column(String(45), unique=True, index=True)
    secondary_email: Mapped[Optional[str]] = mapped_column(String(45))
    password: Mapped[str] = mapped_column(String(100))
    first_name: Mapped[str] = mapped_column(String(20))
    last_name: Mapped[str] = mapped_column(String(20))
    phone_number: Mapped[Optional[str]] = mapped_column(String(15), unique=True)
    birthdate: Mapped[date] = mapped_column(String(10))
    registration_date: Mapped[int] = mapped_column(Integer, insert_default=func.current_timestamp())

    # enums
    role: Mapped[Roles] = mapped_column(Enum(Roles), insert_default=Roles.USER)

    # relationships
    lookup_customer_billings_relationship: Mapped['LookupCustomerBillingsModel'] = \
        relationship(back_populates='customers_relationship')

    def __init__(self, **kwargs):
        super(CustomersModel, self).__init__(**kwargs)


class LookupCustomerBillingsModel(BaseModel):
    # foreign keys
    customer_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('customers.customer_id'), primary_key=True, unique=False, index=True
    )
    billing_profile_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('billing_profiles.billing_profile_id'), primary_key=True, unique=False, index=True
    )
    priority: Mapped[int] = mapped_column(Integer)

    # relationships
    customers_relationship: Mapped['CustomersModel'] = \
        relationship(back_populates='lookup_customer_billings_relationship')

    billing_profiles_relationship: Mapped['BillingProfilesModel'] = \
        relationship(back_populates='lookup_customer_billings_relationship')

    def __init__(self, **kwargs):
        super(LookupCustomerBillingsModel, self).__init__(**kwargs)


class BillingProfilesModel(BaseModel):
    billing_profile_id: Mapped[id] = mapped_column(Integer, primary_key=True, unique=True, autoincrement=True, index=True)
    card_number: Mapped[int] = mapped_column(Integer)
    card_name: Mapped[str] = mapped_column(String(20))
    expiry_date: Mapped[date] = mapped_column(String(10))
    cvv: Mapped[int] = mapped_column(Integer)

    # relationships
    lookup_customer_billings_relationship: Mapped['LookupCustomerBillingsModel'] = \
        relationship(back_populates='billing_profiles_relationship')

    def __init__(self, **kwargs):
        super(BillingProfilesModel, self).__init__(**kwargs)
