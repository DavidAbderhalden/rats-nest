from abc import ABC
from sqlalchemy import TypeDecorator, String


class SQLStrEnum(TypeDecorator, ABC):
    impl = String

    def __init__(self, enumtype, *args, **kwargs):
        super(SQLStrEnum, self).__init__(*args, **kwargs)
        self._enumtype = enumtype

    def process_bind_param(self, value, dialect):
        if isinstance(value, str):
            return value

        return value

    def process_result_value(self, value, dialect):
        return self._enumtype(value)