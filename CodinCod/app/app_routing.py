from sanic import text, json
from sanic.request import Request

from ..game_room import GameRoom
from ..puzzle import Puzzle
from ..exceptions import CodinCodException

from .user.user import User

from bson.objectid import ObjectId
from bson.errors import InvalidId

from . import app

from . import exception_handler
from . import user
from . import game_room
from . import ide


@app.get('/puzzles')
async def puzzle(request: Request):
    args = request.args

    if "id" in args:
        try:
            puzzle_id = ObjectId(args["id"][0])
        except InvalidId:
            raise CodinCodException("Invalid puzzle id")

        puzzle = Puzzle.get_by_id(puzzle_id)
        return json(puzzle.as_dict())

    if "author_id" in args:
        try:
            author_id = ObjectId(args["author_id"][0])
        except InvalidId:
            raise CodinCodException("Invalid user id")
        
        puzzles = Puzzle.get_by_author(author_id)
        return json([puzzle.as_dict() for puzzle in puzzles])
        
    raise CodinCodException("No puzzle_id/author_id was provided")
