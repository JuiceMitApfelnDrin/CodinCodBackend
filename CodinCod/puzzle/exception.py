__all__ = ("PuzzleException", )

from ..exceptions import CodinCodException

class PuzzleException(CodinCodException):
    pass

class PuzzleCreationException(PuzzleException):
    pass

class PuzzleFindException(PuzzleException):
    pass

class TestCaseFindException(PuzzleException):
    pass