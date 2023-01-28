from bson.objectid import ObjectId

from CodinCod.puzzle.puzzle import Puzzle
from CodinCod.puzzle.puzzle_type import PuzzleType
from CodinCod.user.user import User


# test query stuff from db
# ----------------------------------

# Puzzles
print("\nPuzzle by id")
print(Puzzle.get_by_id(puzzle_id=ObjectId("6338b06459d723d748ed7fb1")))

print("\nPuzzles by type")
print(Puzzle.get_by_type(PuzzleType.FASTEST))

print("\nPuzzles by author_id")
print(Puzzle.get_by_author(author_id=ObjectId("6333585a0b6e7d94a0c64ce3")))


# Users
print("\nUser by id")
print(User.get_by_id(user_id=ObjectId("6345b74a6708cb008dd170d4")))

print("\nUsers that include X in nickname")
print(User.get_by_nickname("u"))
