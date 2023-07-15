from __future__ import annotations
from sanic.request import Request
from sanic.exceptions import Unauthorized
from bson.objectid import ObjectId

from ...user import User
from ...user.exception import UserFindException, UserAuthException

def auth(request: Request):
    try:
        token: str = request.cookies["token"]
        user_id: str = request.cookies["user_id"]

    except KeyError:
        raise Unauthorized("User is not logged in!")

    try:
        return User.auth_by_token(ObjectId(user_id), token)
    
    except (UserAuthException, UserFindException):
        raise Unauthorized("Failed to authorize")