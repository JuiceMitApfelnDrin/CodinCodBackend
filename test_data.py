import logging
from bson.objectid import ObjectId
from CodinCod.puzzle.validator_type import ValidatorType

from CodinCod.user.user import User
from CodinCod.database import db_client
from CodinCod.puzzle.puzzle import Puzzle
from CodinCod.puzzle.puzzle_type import PuzzleType
from CodinCod.puzzle.validator import Validator

from pymongo.errors import DuplicateKeyError

from CodinCod.user.exception import UserCreationException
from CodinCod.puzzle.exception import PuzzleException

# example users insert stuff, test data

def create_user(nickname: str, email: str, password: str) -> tuple[User, str] | None:
    try:
        return User.create(
            nickname,
            email,
            password
        )
    except UserCreationException as exception:
        logging.warning(str(exception))

def create_puzzle(title: str, statement: str, constraints: str, validators: list[Validator], puzzle_types: list[PuzzleType], author_id: ObjectId) -> Puzzle | None:
    try:
        return Puzzle.create(
            title = title,
            statement = statement,
            constraints = constraints,
            validators = validators,
            puzzle_types = puzzle_types,
            author_id = author_id
        )
    except PuzzleException as exception:
        logging.warning(str(exception))   


create_user(
    "Gorn10",
    "Gorn10@dings.com",
    "password"
)

puzzle_author = User.get_by_nickname("Gorn10")
assert puzzle_author is not None

create_user(
    "Hydrazer",
    "hydrazer@dings.com",
    "password"
)

create_user(
    "jutyve",
    "jutyve@dings.com",
    "password"
)

create_user(
    "murat",
    "murat@dings.com",
    "password"
)

# example puzzle insert stuff, test data
create_puzzle(
    title = "FizzBuzz",
    statement = "Print numbers from 1 to N, but if the number is divisible by F, print \"Fizz\", and if the number is divisible by B print \"Buzz\". If it is divisible by both print \"FizzBuzz\".",
    constraints = "N lines",
    validators = [
        Validator(type = ValidatorType.TESTCASE, input = "7 2 3",
                  output = "1\nFizz\nBuzz\nFizz\n5\nFizzBuzz\n7"),
        Validator(type = ValidatorType.TESTCASE, input="3 1 1",
                  output = "FizzBuzz\nFizzBuzz\nFizzBuzz"),
        Validator(type = ValidatorType.TESTCASE, input = "10 11 12",
                  output = "1\n2\n3\n4\n5\n6\n7\n8\n9\n10"),
    ],
    puzzle_types =[ PuzzleType.SHORTEST,
                  PuzzleType.FASTEST, PuzzleType.REVERSE],
    author_id = ObjectId(puzzle_author.id)
)
