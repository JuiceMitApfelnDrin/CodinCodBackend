from sanic import json
from sanic.request import Request
from sanic.exceptions import BadRequest

from . import puzzle_blueprint
from ...puzzle import Puzzle
from ...puzzle.exception import TestCaseFindException
from ..user import auth
from ...piston import Language

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

@puzzle_blueprint.post("/run_testcase")
async def run_testcase(request: Request):
    user = auth(request)

    # TODO:  eliminate repetition

    if "puzzle_id" not in request.json:
        raise BadRequest("No puzzle id was provided")
    
    if "id" not in request.json:
        raise BadRequest("No test case id was provided")
    
    if "code" not in request.json:
        raise BadRequest("No code was provided")
    
    if "language" not in request.json:
        raise BadRequest("No language was provided")

    puzzle = Puzzle.get_by_id(request.json["puzzle_id"])

    try:
        success, output = await puzzle.run_testcase(request.json["id"], request.json["code"], Language.get(request.json["language"]))
    
    except TestCaseFindException:
        raise BadRequest("Invalid test case id")
    
    return json({
        "success": success,
        "output": output
    })