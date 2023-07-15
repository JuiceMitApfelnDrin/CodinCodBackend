__all__ = ("ide_blueprint", )

from typing import Final
from sanic import Blueprint

ide_blueprint: Final = Blueprint('ide', url_prefix='/')

from . import language