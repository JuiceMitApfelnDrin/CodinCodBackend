from __future__ import annotations

__all__ = ("GameRoomException", "GameLaunchException")

from ..exceptions import CodinCodException

class GameRoomException(CodinCodException):
    pass

class GameLaunchException(CodinCodException):
    pass