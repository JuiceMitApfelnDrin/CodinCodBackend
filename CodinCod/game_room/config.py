from __future__ import annotations
from dataclasses import dataclass

from ..puzzle.puzzle_type import PuzzleType
from ..submission.language import Language
# from puzzle.puzzle_difficulty import Difficulty
from .visibility import GameRoomVisibility
from ..game_room import visibility

# TODO: for version 0.2.0:
# difficulty: Difficulty = Difficulty.RANDOM
# max_players: int = 50


@dataclass
class GameRoomConfig:
    game_mode: PuzzleType
    languages: tuple[Language]

    duration_minutes: int = 15
    visibility: GameRoomVisibility = GameRoomVisibility.PUBLIC

    @classmethod
    def from_dict(cls, info: dict) -> GameRoomConfig:
        game_mode_name = info["game_mode"]
        visibility_name = info["visibility"]
        return cls(
            game_mode = PuzzleType[game_mode_name],
            languages = tuple(Language.get(lang_name) for lang_name in info["langugaes"]),
            duration_minutes = info["duration_minutes"],
            visibility = GameRoomVisibility(visibility_name)
        )


    def as_dict(self) -> dict:
        return {
            "game_mode": self.game_mode.name,
            "languages": tuple(lang.name for lang in self.languages),
            "duration_minutes": self.duration_minutes,
            "visiblitity": self.visibility.name
        }