"""Custom date schema"""
import re

from typing import Any

from typing_extensions import Annotated

from pydantic.functional_validators import AfterValidator

def is_valid_date(value: Any) -> bool:
    assert bool(
        re.search(r'(0[1-9]|[12][0-9]|3[01])\.(0[1-9]|1[1,2])\.(19|20)\d{2}', value)
    ), f'{value} is not in the date format dd.mm.yyyy'
    return value

CustomDate = Annotated[str, AfterValidator(is_valid_date)]
