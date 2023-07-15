from sanic import json
from sanic.request import Request
from sanic.exceptions import BadRequest

from . import puzzle_blueprint
from ...puzzle import Puzzle

from bson.objectid import ObjectId
from bson.errors import InvalidId


@puzzle_blueprint.get('/puzzles')
async def puzzle(request: Request):
    args = request.args

    if "id" in args:
        try:
            puzzle_id = ObjectId(args["id"][0])
        except InvalidId:
            raise BadRequest("Invalid puzzle id")

        puzzle = Puzzle.get_by_id(puzzle_id)
        return json(puzzle.as_dict())

    if "author_id" in args:
        try:
            author_id = ObjectId(args["author_id"][0])
        except InvalidId:
            raise BadRequest("Invalid user id")
        
        puzzles = Puzzle.get_by_author(author_id)
        return json([puzzle.as_dict() for puzzle in puzzles])
        
    raise BadRequest("No puzzle_id/author_id was provided")
