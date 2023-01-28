from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, cast, Any

from bson.objectid import ObjectId
from pymongo.errors import DuplicateKeyError

from . import PuzzleType, PuzzleDifficulty, puzzles_collection
from .exception import PuzzleException, PuzzleCreationException, PuzzleFindException

from .validator import Validator

@dataclass(eq=False, kw_only=True)
class Puzzle:
    _id: ObjectId
    title: str
    statement: str
    constraints: str
    author_id: ObjectId
    validators: list[Validator]
    puzzle_types: list[PuzzleType]

    # default difficulty = medium
    # TODO: for version 0.2.0:
    # update difficulty based of percentage of people failing/passing in a game
    difficulty: PuzzleDifficulty = PuzzleDifficulty.MEDIUM

    @property
    def id(self) -> ObjectId:
        return self._id

    @classmethod
    def create(cls, title: str, statement: str, constraints: str, validators: list[Validator],
                puzzle_types: list[PuzzleType], author_id: ObjectId) -> Puzzle:

        try:
            result = puzzles_collection.insert_one(
                {
                    "title": title,
                    "statement": statement,
                    "constraints": constraints,
                    "author_id": author_id,
                    "validators":  [validator.as_dict() for validator in validators],
                    "puzzle_types": [puzzle_type.name for puzzle_type in puzzle_types],
                }
            )
        except DuplicateKeyError as duplicate_error:
            details = duplicate_error.details
            assert details is not None

            key_pattern = details["keyPattern"]
            duplicate_keys = ', '.join(key_pattern)

            if len(key_pattern) > 1:
                error_message = duplicate_keys + " are taken"
            else:
                error_message = duplicate_keys + " is taken"

            raise PuzzleCreationException(error_message)

        return cls.get_by_id(result.inserted_id)

    @classmethod
    def from_dict(cls, info: dict) -> Puzzle:
        return cls(
            _id = ObjectId(info["_id"]),
            title = info["title"],
            statement = info["statement"],
            constraints = info["constraints"],
            author_id = info["author_id"],
            validators = info["validators"],
            puzzle_types = [PuzzleType[puzzle_type]
                for puzzle_type in info["puzzle_types"]])

    @classmethod
    def get_by_id(cls, puzzle_id: ObjectId) -> Puzzle:
        puzzle_info = cls.get_puzzle_info_from_db(puzzle_id)
        return Puzzle.from_dict(puzzle_info)

    @classmethod
    def get_puzzle_info_from_db(cls, puzzle_id: ObjectId) -> dict[str, Any]:
        info = puzzles_collection.find_one({"_id": puzzle_id})
        if info is None:
            raise PuzzleFindException("Can't find puzzle")

        return cast(dict[str, Any], info)

    @classmethod
    def get_by_author(cls, author_id: ObjectId) -> tuple[Puzzle, ...]:
        cursor = puzzles_collection.find(
            {"author_id": author_id})
        return tuple(map(Puzzle.from_dict, cursor))

    @classmethod
    def get_by_type(cls, puzzle_type: PuzzleType) -> Puzzle:
        """
        raises an error if there is no puzzles of that type
        """
        # TODO: catch the exception
        pipeline = [
            {
                "$match":
                    {
                        "puzzle_types": {
                            "$in": [puzzle_type.value]
                        }
                    }
            },
            {
                "$sample": {
                    "size": 1
                }
            },
        ]
        cursor = puzzles_collection.aggregate(pipeline)
        return Puzzle.from_dict(cursor.next())

    def as_dict(self) -> dict:
        """
        Return a represention of the game room that can be sent
        to the client.
        """

        # TODO: add validators
        return {
            "_id": str(self.id),
            "title": self.title,
            "statement": self.statement,
            "constraints": self.constraints,
            "author_id": str(self.author_id),
            "puzzle_types": [puzzle_type.name for puzzle_type in self.puzzle_types]
        }
