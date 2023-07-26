__all__ = ("game_room_blueprint",)

from typing import Final
from sanic import Blueprint

game_room_blueprint: Final = Blueprint('game_room', url_prefix='/game_room')

from . import game_room