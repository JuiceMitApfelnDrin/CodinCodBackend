# TODO: this doesn't work here
from dataclasses import asdict as asdict_
from bson.objectid import ObjectId
__all__ = ["static_init"]

from typing import Protocol, TypeVar


class Proto(Protocol):
    @classmethod
    def static_init(cls):
        pass


P = TypeVar("P", bound=Proto)


def static_init(cls: P) -> P:
    cls.static_init()
    return cls