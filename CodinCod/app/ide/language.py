from __future__ import annotations

from sanic import json
from sanic.request import Request

from . import ide_blueprint

from ...piston import Language

@ide_blueprint.get('/languages')
async def login(request: Request):
    return json(Language.all())
