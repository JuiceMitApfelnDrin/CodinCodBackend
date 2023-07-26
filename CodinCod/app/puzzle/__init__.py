__all__ = ("puzzle_blueprint", )

from typing import Final
from sanic import Blueprint

puzzle_blueprint: Final = Blueprint('puzzle', url_prefix='/puzzle')

from . import puzzle