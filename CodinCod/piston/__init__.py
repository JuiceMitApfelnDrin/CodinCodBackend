__all__ = ("piston", "Language")

from pistonapi import PistonAPI
from typing import Final

piston: Final = PistonAPI()

from .language import Language