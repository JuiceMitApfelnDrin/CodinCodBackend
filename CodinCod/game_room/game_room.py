from __future__ import annotations

from datetime import datetime, timedelta
from dataclasses import dataclass, field

from typing import Optional, cast, ClassVar, Any
from bson.objectid import ObjectId

from . import GameRoomState, GameRoomVisibility, GameRoomConfig
from . import games_collection
from .exception import GameRoomException, GameLaunchException

from ..submission import Submission
from ..puzzle import Puzzle

from ..user import User
from ..session import Session, SessionException
from ..submission import SubmissionException


# TODO: for version 0.2.0:
# submitted_at: int => allow users to submit one last time after round ends?

# TODO: update to raise exceptions instead of returning None

@dataclass(eq=False, kw_only=True)
class GameRoom:
    __active_gamerooms: ClassVar[dict[ObjectId, GameRoom]]

    _id: ObjectId
    creator: User
    config: GameRoomConfig
    puzzle: Puzzle

    start_time: datetime
    state: GameRoomState

    players: dict[ObjectId, User]
    submissions: dict[ObjectId, Submission]

    # includes both players sessions and spectators
    sessions: dict[User, set[Session]] = field(default_factory=dict)

    @property
    def id(self):
        return self._id

    @property
    def end_time(self) -> datetime:
        """Returns the end time """
        return self.start_time + timedelta(minutes=self.config.duration_minutes)

    @classmethod
    def create(cls, *, creator: User, puzzle: Puzzle, config: GameRoomConfig, start_time: datetime) -> GameRoom:
        """
        Creates a new gameroom and store it in db. 
        """
        result = games_collection.insert_one(
            {
                "creator_id": creator.id,
                "puzzle_id": puzzle.id,
                "config": config.as_dict(),
                "start_time": start_time.isoformat(),
                "game_state": GameRoomState.WAITING_FOR_PLAYERS.name,
                "players_ids": [],
                "submissions_ids": []
            }
        )
        game_room = cls.get_from_db_by_id(result.inserted_id)
        assert game_room is not None
        return game_room

    @classmethod
    def get_by_id(cls, gameroom_id: ObjectId) -> GameRoom:
        """
        Tries to find a GameRoom object with the given id from memory and db.
        Returns None if no active GameRoom with that id exists.
        """
        game_room = cls.get_active_gameroom(gameroom_id)
        if game_room is not None:
            return game_room
        
        return cls.get_from_db_by_id(gameroom_id)

    @classmethod
    def get_from_db_by_id(cls, gameroom_id: ObjectId) -> GameRoom:
        """
        Tries to find a GameRoom object with the given id from memory.
        Returns None if no active GameRoom with that id exists.
        """
        info = games_collection.find_one({"_id": gameroom_id})

        if info is None:
            raise GameRoomException("Can't find GameRoom")

        info = cast(dict[str, Any], info)
        return cls.from_db_dict(info)

    @classmethod
    def from_db_dict(cls, info: dict):
        creator = User.get_by_id(info["creator_id"])
        puzzle = Puzzle.get_by_id(info["puzzle_id"])

        players = {}
        for player_id in info["players_ids"]:
            player = User.get_by_id(player_id)
            players[player_id] = player

        submissions = {}
        for submission_id in info["submissions_ids"]:
            submission = Submission.get_by_id(submission_id)
            # TODO: remove after updating submission API
            assert submission is not None
            submissions[submission_id] = submissions
        
        return cls(
            _id = info["_id"],
            config = GameRoomConfig.from_dict(info["config"]),
            creator = creator,
            puzzle = puzzle,
            start_time = datetime.fromisoformat(info["start_time"]),
            state = GameRoomState[info["state"]],
            players = players,
            submissions = submissions
        )

    @classmethod
    def get_active_gameroom(cls, gameroom_id: ObjectId) -> GameRoom:
        """
        Tries to find a GameRoom object with the given id from memory.
        Returns None if no active GameRoom with that id exists
        (it may still exist in the database).
        """
        if gameroom_id not in cls.__active_gamerooms:
            raise GameRoomException("Can't find GameRoom")

        return cls.__active_gamerooms[gameroom_id]

    def as_db_dict(self) -> dict[str, Any]:
        """
        Return a representation of the game room that can be inserted
        into a MongoDB collection using .insert_one() method.
        """
        return {
            "_id": self.id,
            "creator_id": self.creator.id,
            "config": self.config.as_dict(),
            "puzzle": self.puzzle.id,
            "start_time": self.start_time.isoformat(),
            "submissions_ids": list(self.submissions.keys()),
            "players_ids": list(self.submissions.keys())
        }
    
    def as_dict(self) -> dict[str, Any]:
        """
        Return a represention of the game room that can be sent
        to the client.
        """
        players = []
        for player in self.players.values():
            player_info = player.public_info()

            submission = next((
                submission for submission in self.submissions.values()
                if submission.user_id == player.id
            ), None)

            if submission is not None:
                player_info["submission"] = submission.public_info()

            players.append(player_info)

        return {
            "_id": str(self.id),
            "config": self.config.as_dict(),
            "puzzle": self.puzzle.id,
            "start_time": self.start_time.isoformat(),
            "players": players
        }

    def add_session(self, session: Session):
        """
        Add session to gameroom.
        This makes the session recieve updates about the game.
        NOT JOINING THE GAME ROOM
        """
        self.sessions[session.user].add(session)

    def remove_session(self, session: Session):
        """
        Remove session from gameroom.
        Raises an excpetion if session is not in sessions.
        """
        user = session.user
        self.sessions[user].remove(session)

        if self.sessions[user]: return
        del self.sessions[user]

        if self.state is not GameRoomState.WAITING_FOR_PLAYERS or\
            user.id not in self.players:
            return
        self.remove_player(user)

    def add_player(self, user: User):
        """
        TODO: add docstring
        """
        # This stops bots from joining, and prevents weird bugs.
        if user in self.sessions:
            raise SessionException(
                "Can't join: the user doesn't have any sessions connected to gameroom!")

        state = self.state
        visibility = self.config.visibility

        if not (state is GameRoomState.WAITING_FOR_PLAYERS or
                state is GameRoomState.IN_PROGRESS and
                visibility is GameRoomVisibility.PRIVATE):
            raise SessionException(
                "Can't join: game already started!")

        self.players[user.id] = user
        # TODO: update frontend

    def remove_player(self, user: User):
        """
        TODO: add docstring
        """
        if user.id not in self.players:
            raise SessionException(
                "Can't remove player from Game: User is not in gameroom!")

        if not self.state is GameRoomState.WAITING_FOR_PLAYERS:
            raise SessionException(
                "Can't remove player from Game: Game has already started!")
        
        del self.players[user.id]
        # TODO: update frontend through websockets

    def add_submission(self, submission: Submission):
        """
        Adds a new submission to the game room. The submission should
        be validated and scored before adding it to the game room.
        Raises an exception when trying to add a submission while the
        game is not in progress.
        """
        state = self.state
        if state is GameRoomState.WAITING_FOR_PLAYERS:
            raise SubmissionException(
                "Can't add submission: Game hasn't started yet!")
        if state is GameRoomState.FINISHED:
            raise SubmissionException(
                "Can't add submission: Game is already finalized!")
        self.submissions[submission.id] = submission

    def launch_game(self, start_time: datetime | None = None):
        """
        Sets the start time for the game to current datetime.
        After calling the game room starts accepting submissions.
        Called when the host decides the game has enough players to start.
        """
        if self.state is not GameRoomState.WAITING_FOR_PLAYERS:
            raise GameLaunchException("Game is already started!")
        
        if self.start_time < datetime.now() + timedelta(seconds = 10):
            raise GameLaunchException("Game is already starting")

        if start_time is None:
            self.start_time = datetime.now() + timedelta(seconds = 5)
        else:
            self.start_time = start_time