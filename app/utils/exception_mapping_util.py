"""Exceptions are handled by this util"""
from enum import StrEnum


class ExceptionType(StrEnum):
    INTEGRITY_ERROR: str = 'IntegrityError'
    UNKNOWN_ERROR: str = 'UnknownError'
    NO_RESULT_FOUND: str = 'NoResultFound'

class ExceptionMapEntry:
    exception_code: int
    exception_message: str

    def __init__(self, exc_code: int, exc_msg: str):
        self.exception_code = exc_code
        self.exception_message = exc_msg

class ExceptionMappingUtil:
    exceptions_map: dict[ExceptionType, ExceptionMapEntry] = {
        ExceptionType.INTEGRITY_ERROR: ExceptionMapEntry(exc_code=400, exc_msg='Already exists'),
        ExceptionType.UNKNOWN_ERROR: ExceptionMapEntry(exc_code=500, exc_msg='An unexpected error occurred'),
        ExceptionType.NO_RESULT_FOUND: ExceptionMapEntry(exc_code=404, exc_msg='No data found'),
    }

    @classmethod
    def get_exception_message(cls, exception: ExceptionType) -> str:
        return cls.exceptions_map[exception].exception_message

    @classmethod
    def get_exception_code(cls, exception: ExceptionType) -> int:
        return cls.exceptions_map[exception].exception_code

    @classmethod
    def get_exception_type(cls, exception: Exception):
        exception_type_string: str = type(exception).__name__
        try:
            exception_type: ExceptionType = ExceptionType(exception_type_string)
            return exception_type
        except (ValueError, AttributeError):
            return ExceptionType.UNKNOWN_ERROR
