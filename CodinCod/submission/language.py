from __future__ import annotations
from enum import Enum
from typing import ClassVar
from dataclasses import dataclass
from urllib import response

from . import piston
from ..utils import static_init


@static_init
@dataclass
class Language:
    __languages: ClassVar[dict[str, Language]] = {}

    name: str
    version: str
    aliases: list[str]
    runtime: str

    @classmethod
    def static_init(cls):
        languages: dict[str, dict] = piston.languages

        for lang_name, lang_infos in languages.items():
            lang_version = lang_infos["version"]
            lang_aliases = lang_infos["aliases"]
            lang_runtime = lang_infos.get("runtime", "")

            if not (type(lang_name) is str and
                    type(lang_version) is str and
                    type(lang_runtime) is str and
                    type(lang_aliases) is list and
                    all(type(alias) is str
                        for alias in lang_aliases)):
                raise TypeError("Piston API: wrong response type")

            # Do we really want to allow all languages ?
            # There is probably rate limits

            language = cls(lang_name, lang_version, lang_aliases, lang_runtime)
            cls.__languages[language.name] = language

    @classmethod
    def get(cls, name: str):
        return cls.__languages[name]

    @classmethod
    def all(cls):
        return tuple(language.as_dict() for language in cls.__languages.values())

    def as_dict(self):
        return {
            "name": self.name,
            "version": self.version,
            "aliases": self.aliases,
            "version": self.version
        }