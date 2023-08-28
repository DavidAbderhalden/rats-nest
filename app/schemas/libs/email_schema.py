"""Custom email schema"""
import re

from typing import Any

from typing_extensions import Annotated

from pydantic.functional_validators import AfterValidator

def is_valid_email_address(value: Any) -> bool:
    assert bool(
        re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b', value)
    ), f'{value} is not an email address'
    return value

Email = Annotated[str, AfterValidator(is_valid_email_address)]
