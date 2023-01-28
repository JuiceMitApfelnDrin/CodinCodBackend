from __future__ import annotations

from ..exceptions import CodinCodException


class SessionException(CodinCodException):
    pass

class InvalidMessageException(SessionException):
    pass