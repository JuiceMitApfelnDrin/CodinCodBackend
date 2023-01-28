__all__ = ("UserException", "UserCreationException", "UserFindException", "UserAuthException")

from ..exceptions import CodinCodException

class UserException(CodinCodException):
    pass

class UserCreationException(UserException):
    pass

class UserFindException(UserException):
    pass

class UserAuthException(UserException):
    pass