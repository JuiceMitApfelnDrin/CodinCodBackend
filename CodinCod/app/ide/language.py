from __future__ import annotations

from typing import Any, Final

from sanic import text, json
from sanic.response import HTTPResponse, redirect
from sanic.request import Request

from bson.objectid import ObjectId
from bson.errors import InvalidId
from pymongo.errors import DuplicateKeyError

from .. import app
from ...submission.language import Language


@app.get('/languages')
async def login(request: Request):
    return json(Language.all())
