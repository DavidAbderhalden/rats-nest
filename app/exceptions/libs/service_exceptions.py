"""Custom exceptions thrown by service instances"""
from app.schemas.libs import Email
from ..rats_nest_error import RatsNestError


class UnverifiedEmailError(RatsNestError):
    def __init__(self, email: Email):
        message: str = f'The email address {email} has not been verified. Please make sure to verify your email address'
        super().__init__(message)

class NoClientHostError(RatsNestError):
    def __init__(self, message: str = 'No client host was provided'):
        super().__init__(message)

class AuthenticationError(RatsNestError):
    def __init__(self, message: str = 'Wrong credentials where used'):
        super().__init__(message)

class InvalidRefreshToken(RatsNestError):
    def __init__(self, message: str = 'The refresh token in invalid'):
        super().__init__(message)

class RefreshError(RatsNestError):
    def __init__(self, message: str = 'Your session has expired'):
        super().__init__(message)
