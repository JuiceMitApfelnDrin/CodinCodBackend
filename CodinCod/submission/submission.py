from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from time import time
from typing import Any, Optional, cast, Final
from bson.objectid import ObjectId

from .language import Language
from . import submissions_collection

@dataclass
class Submission:
    _id: ObjectId
    puzzle_id: ObjectId
    user_id: ObjectId
    code: str
    language: Language
    submitted_at: datetime

    validators: list[bool] = field(default_factory=list)
    execution_finished: bool = False
    _max_code_size: Final = 9001

    @property
    def id(self):
        return self._id

    @property
    def time(self) -> datetime:
        return self.submitted_at

    @property
    def code_size(self) -> int:
        return len(self.code)

    @property
    def score(self) -> Optional[float]:
        if not self.execution_finished:
            return None
        return sum(self.validators)/len(self.validators)

    @classmethod
    def create(cls, user_id, puzzle_id, language: Language, code) -> Optional[Submission]:
        timestamp = datetime.now().isoformat()
        result = submissions_collection.insert_one(
            {
                "user_id": user_id,
                "puzzle_id": puzzle_id,
                "language": language.name,
                "code": code,
                "submitted_at": timestamp
            }
        )
        submission = Submission.get_by_id(result.inserted_id)
        return submission

    @classmethod
    def get_by_id(cls, submission_id: ObjectId) -> Optional[Submission]:
        return cls.get_from_db_by_id(submission_id)

    @classmethod
    def get_from_db_by_id(cls, submission_id: ObjectId) -> Optional[Submission]:
        info = cast(Optional[dict], submissions_collection.find_one({"_id": submission_id}))
        if info is None: return
        return cls.get_from_db_dict(info)

    @classmethod
    def get_from_db_dict(cls, info) -> Submission:
        return cls(
            ObjectId(info["_id"]),
            ObjectId(info["puzzle_id"]),
            ObjectId(info["user_id"]),
            info["code"],
            Language.get(info["language"]),
            datetime.fromisoformat(info["submitted_at"])
        )

    def as_dict(self) -> dict[str, Any]:
        return {
            "_id": str(self._id),
            "puzzle_id": self.puzzle_id,
            "user_id": self.user_id,
            "code": self.code,
            "language": self.language.name,
            "submitted_at": self.submitted_at
        }

    def public_info(self) -> dict[str,Any]:
        return {
            "_id": str(self._id),
            "puzzle_id": self.puzzle_id,
            "user_id": self.user_id,
            "language": self.language.name,
            "submitted_at": self.submitted_at
        }

    async def execute_testcases(self, puzzle):
        # execute for each validator the code
        # aka does the code work or not for a given Validator?
        assert puzzle is not None
        for validator in puzzle.validators:
            success, _ = await validator.execute(self.code, self.language)
            self.validators.append(success)

        self.execution_finished = True