from typing import Any, Final

import re

from sanic import text, json
from sanic.response import HTTPResponse, redirect
from sanic.request import Request

from bson.objectid import ObjectId
from bson.errors import InvalidId

from validate_email import validate_email

from .. import app

from ...user import User
from ...exceptions import CodinCodException

@app.get('/users')
async def users(request: Request):
    args = request.args
    if "id" in args:
        try:
            user_id = ObjectId(args["id"][0])
        except InvalidId:
            raise CodinCodException("Invalid user id!")
            
        user = User.get_by_id(user_id)
        return json(user.public_info())

    if "search_by_nickname" in args:
        users = User.get_list_by_nickname(
            str(args["search_by_nickname"][0]))

        transformed_users = []
        for user in users:
            transformed_users.append(user.public_info())

        return json(transformed_users)

    if "nickname" in args:
        user = User.get_by_nickname(str(args["nickname"][0]))
        return json(user.public_info())

    return text("Invalid request: missing arguments", status = 400)


@app.post('/register')
async def register(request: Request):
    content:  dict[str, Any] = request.json
    nickname: str = content["nickname"]
    password: str = content["password"]
    email:    str = content["email"]


    if not validate_email(
        email_address=email,
        check_smtp=False
    ):
        return text("Email is not valid", status = 400)

    user, token = User.create(
        nickname=nickname,
        email=email,
        password=password
    )

    response = HTTPResponse()
    response.cookies["token"] = token

    return response


# WIP! Didn't test this at all!
@app.post('/login')
async def login(request: Request):
    content:  dict[str, Any] = request.json
    nickname: str = content["nickname"]
    password: str = content["password"]

    user = User.get_by_nickname(nickname)
    if user is None:
        return text("Password or Nickname is incorrect", status = 400)

    iscorrect, token = user.verify_password(password)
    if not iscorrect:
        return text("Password or Nickname is incorrect", status = 400)

    response = HTTPResponse()
    response.cookies["token"] = token

    return response