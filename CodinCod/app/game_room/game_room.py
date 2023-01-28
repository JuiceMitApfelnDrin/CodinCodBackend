from __future__ import annotations

from sanic import text, json
from sanic.response import HTTPResponse
from sanic.request import Request

from bson.objectid import ObjectId
from bson.errors import InvalidId

from .. import app
from ..user import auth

from ...game_room import GameRoom
from ...puzzle import Puzzle
from ...exceptions import CodinCodException


@app.get('/game_info')
async def game_info(request: Request) -> HTTPResponse:
    args = request.args
    if "id" not in args:
        return text("No game id was provided", status=400)

    try:
        game_id = ObjectId(args["id"][0])
    except InvalidId:
        raise CodinCodException("Invalid game id!")

    game = GameRoom.get_by_id(game_id)
    return json(game.as_dict())


@app.post('/game_join')
async def game_join(request: Request) -> HTTPResponse:
    user = auth(request)

    try:
        game_id = ObjectId(request.json["id"])
    except InvalidId:
        raise CodinCodException("Invalid game id!")
        
    game = GameRoom.get_by_id(game_id)
    game.add_player(user)
    
    return json(game.as_dict())


@app.post('/game_start')
async def game_start(request: Request) -> HTTPResponse:
    user = auth(request)
    
    try:
        game_id = ObjectId(request.json["id"])
    except InvalidId:
        raise CodinCodException("Invalid game id!")

    game = GameRoom.get_by_id(game_id)
    if game.creator is not user:
        raise CodinCodException("Only the game creator is allowed to start the game!")
    
    game.launch_game()

    return HTTPResponse()


@app.post('/game_leave')
async def game_leave(request: Request) -> HTTPResponse:
    user = auth(request)

    try:
        game_id = ObjectId(request.json["id"])
    except InvalidId:
        raise CodinCodException("Invalid game id!")

    game = GameRoom.get_by_id(game_id)
    game.remove_player(user)
    
    return HTTPResponse()
