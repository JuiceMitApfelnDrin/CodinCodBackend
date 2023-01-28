from __future__ import annotations

from typing import Any, Final

from sanic import text, json
from sanic.response import HTTPResponse, redirect
from sanic.request import Request

from bson.objectid import ObjectId
from pymongo.errors import DuplicateKeyError

from validate_email import validate_email
from urllib.parse import urlencode

from .. import app

from ...user import User

def auth(request: Request):
    # If can't find "token"/ "user_id" it raises an Internal Error
    token: str = request.cookies["token"]
    user_id: str = request.cookies["user_id"]

    return User.auth_by_token(ObjectId(user_id), token)