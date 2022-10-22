from sanic import text, json, response
from sanic.request import Request

from ..user import User

from bson.objectid import ObjectId
from bson.errors import InvalidId
from validate_email import validate_email
from urllib.parse import urlencode

from . import app

@app.get('/users')
async def users(request: Request):
    args = request.args
    if "id" not in args:
        return text("No id was provided", status=400)

    try:
        user = User.get_by_id(ObjectId(args["id"][0]))
    except InvalidId:
        user = None
        
    if user is None:
        return text("Can't find user", status=400)

    return json(user.public_info())

# WIP! Didn't test this at all!
@app.get('/register')
async def register(request: Request):
    content = request.json
    nickname: str = content["nickname"]
    password: str = content["password"]
    email:    str = content["email"]
    
    if not 8 <= len(password) <= 64:
        return text("Password must be between 8 and 64 characters")

    # TODO: Change check_smtp to True, after getting smtp server!
    if not validate_email(
        email_address=email,
        check_smtp=False):
        return text("Email is not valid", status=400)

    try:
        user, token = User.create(
            nickname=nickname,
            email=email,
            password=password)
    except Exception: 
        # TODO: remove Exception because it's not safe
        return text("Email or Nickname is taken", status=400)

    return response.redirect(to="/",headers={"set-cookie":urlencode({"token": token})})