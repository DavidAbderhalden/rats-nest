import re

from app.models import Countries

from typing import Any, Optional
from typing_extensions import Annotated

from pydantic import BaseModel
from pydantic.functional_validators import AfterValidator


def is_valid_email_address(value: Any) -> bool:
    assert bool(
        re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b', value)
    ), f'{value} is not an email address'
    return value

def is_valid_date(value: Any) -> bool:
    assert bool(
        re.search(r'(0[1-9]|[12][0-9]|3[01])\.(0[1-9]|1[1,2])\.(19|20)\d{2}', value)
    ), f'{value} is not in the date format dd.mm.yyyy'
    return value

Email = Annotated[str, AfterValidator(is_valid_email_address)]
CustomDate = Annotated[str, AfterValidator(is_valid_date)]


class AddressSchema(BaseModel):
    country_code: Countries
    city_name: str
    zip_code: int
    street_name: str
    house_number: int


class PostAccountsRegisterSchema(BaseModel):
    username: str
    primary_email: Email
    secondary_email: Optional[Email] = None
    password: str
    first_name: str
    last_name: str
    phone_number: Optional[str] = None
    birthdate: CustomDate
    delivery_address: AddressSchema
    home_address: AddressSchema
