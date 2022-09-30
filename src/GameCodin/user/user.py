from __future__ import annotations

from dataclasses import dataclass, asdict, field
from typing import ClassVar
from bson.objectid import ObjectId

from GameCodin.database.collection import Collection
from .profile import Profile
from ..database import db_client


@dataclass
class User:
    #
    __current_users: ClassVar[dict[ObjectId, User]] = {}

    user_id: ObjectId
    user_token: str  # to authenicate
    username: str
    email: str

    # TODO: for version 2.0:
    # profile: Profile

    @property
    def dict(self):
        return asdict(self)

    @classmethod
    def get_by_id(cls, user_id: ObjectId) -> User:
        if user_id in cls.__current_users:
            return cls.__current_users[user_id]

        user_infos = cls.get_infos_from_db(user_id)
        # TODO: create User from infos
        return user_infos

    @classmethod
    def get_infos_from_db(cls, user_id: ObjectId) -> dict:
        return db_client[Collection.USERS.value].find_one({"_id": user_id})

    def __post_init__(self):
        self.__ref_count = 0

    @property
    def ref_count(self):
        """
        TODO: decide
        ref_count keeps track of number of times the user is refrenced
        somewhere to decide if it should be kept alive we want only
        users that are online or in a gameroom that didn't end yet
        to be kept in memory otherwise load it from database when its needed.
        why do we this ? Keeping all users in mem doesn't make sense
        + because the gamerooms have lists of users not their ids
        so we need to keep those in memory. 
        I think that using ids and create a temp User object from db whenever need it
        might be a better idea ?
        """
        return self.__ref_count

    def acquire(self):
        if not self.__ref_count:
            self.__current_users[self.user_id] = self
        self.__ref_count += 1

    def release(self):
        self.__ref_count -= 1
        if not self.__ref_count:
            del self.__current_users[self.user_id]
