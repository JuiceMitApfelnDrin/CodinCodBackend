from __future__ import annotations
from enum import Enum


class GameRoomState(Enum):
    WAITING_FOR_PLAYERS = 0
    IN_PROGRESS = 1
    PROCESSING_FINAL_SUBMISSIONS = 2
    FINISHED = 3
