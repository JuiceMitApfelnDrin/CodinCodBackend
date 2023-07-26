__all__ = ("auth", "user_blueprint")

from typing import Final
from sanic import Blueprint

from .auth import auth

user_blueprint: Final = Blueprint('user', url_prefix='/user')

from . import user