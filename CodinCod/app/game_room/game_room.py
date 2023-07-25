from __future__ import annotations

from sanic import text, json
from sanic.response import HTTPResponse
from sanic.request import Request
from sanic.exceptions import BadRequest
from bson.objectid import ObjectId
from bson.errors import InvalidId

from . import game_room_blueprint

from ..user import auth
from ...game_room import GameRoom


@game_room_blueprint.get('/game_info')
async def game_info(request: Request) -> HTTPResponse:
    args = request.args

    if "id" not in args:
        raise BadRequest("No game id was provided")

    try:
        game_id = ObjectId(args["id"][0])
    except InvalidId:
        raise BadRequest("Invalid game id!")

    game = GameRoom.get_by_id(game_id)
    return json(game.as_dict())


@game_room_blueprint.post('/game_join')
async def game_join(request: Request) -> HTTPResponse:
    user = auth(request)

    if "id" not in request.json:
        raise BadRequest("No game id was provided")

    try:
        game_id = ObjectId(request.json["id"])
    except InvalidId:
        raise BadRequest("Invalid game id!")

    game = GameRoom.get_by_id(game_id)
    game.add_player(user)

    return json(game.as_dict())


@game_room_blueprint.post('/game_start')
async def game_start(request: Request) -> HTTPResponse:
    user = auth(request)

    if "id" not in request.json:
        raise BadRequest("No game id was provided")

    try:
        game_id = ObjectId(request.json["id"])
    except InvalidId:
        raise BadRequest("Invalid game id!")

    game = GameRoom.get_by_id(game_id)
    if game.creator is not user:
        raise BadRequest("Only the game creator is allowed to start the game!")

    game.launch_game()

    return HTTPResponse()


@game_room_blueprint.post('/game_leave')
async def game_leave(request: Request) -> HTTPResponse:
    user = auth(request)

    if "id" not in request.json:
        raise BadRequest("No game id was provided")

    try:
        game_id = ObjectId(request.json["id"])
    except InvalidId:
        raise BadRequest("Invalid game id!")

    game = GameRoom.get_by_id(game_id)
    game.remove_player(user)

    return HTTPResponse()
