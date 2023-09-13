"""Base class for any internal custom exceptions"""
class RatsNestError(Exception):
    message: str

    def __init__(self, message: str = 'An application error was raised'):
        self.message = message
        super().__init__(self.message)
