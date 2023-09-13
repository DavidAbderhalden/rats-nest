"""Exceptions are handled by this util"""
from enum import StrEnum

from exceptions.libs.service_exceptions import RefreshError, UnverifiedEmailError, AuthenticationError, \
    NoClientHostError


class ExceptionType(StrEnum):
    INTEGRITY_ERROR: str = 'IntegrityError'
    UNKNOWN_ERROR: str = 'UnknownError'
    NO_RESULT_FOUND: str = 'NoResultFound'
    NO_CLIENT_HOST_ERROR: str = 'NoClientHostError'
    AUTHENTICATION_ERROR: str = 'AuthenticationError'
    UNVERIFIED_EMAIL_ERROR: str = 'UnverifiedEmailError'
    INVALID_REFRESH_TOKEN: str = 'InvalidRefreshToken'
    REFRESH_ERROR: str = 'RefreshError'

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
        ExceptionType.NO_CLIENT_HOST_ERROR: ExceptionMapEntry(exc_code=400, exc_msg=NoClientHostError().message),
        ExceptionType.AUTHENTICATION_ERROR: ExceptionMapEntry(exc_code=401, exc_msg=AuthenticationError().message),
        ExceptionType.UNVERIFIED_EMAIL_ERROR: ExceptionMapEntry(
            exc_code=401,
            exc_msg=UnverifiedEmailError(email='provided').message
        ),
        ExceptionType.INVALID_REFRESH_TOKEN: ExceptionMapEntry(exc_code=401, exc_msg='The refresh token in invalid'),
        ExceptionType.REFRESH_ERROR: ExceptionMapEntry(
            exc_code=401,
            exc_msg=RefreshError().message
        ),
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
