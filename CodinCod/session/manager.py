from __future__ import annotations
from ..game_room.game_room import GameRoom
from dataclasses import dataclass, field
from requests import request

from sanic.server.websockets.impl import WebsocketImplProtocol
from websockets.exceptions import ConnectionClosed
from sanic.request import Request

import asyncio
from typing import Final, ClassVar, Optional
from . import Session, Message, MessageType, SessionException
from ..user import User
from ..game_room import GameRoom
from ..exceptions import CodinCodException

class SessionManager(Session):
    gameroom: Optional[GameRoom]
    
    async def ws_handler(self):
        try:
            while True:
                try:
                    message = await self.recv()
                    await self.packet_handler(message)
                    
                except CodinCodException as exception:
                    # await self.send_error(exception.__class__.__name__, str(exception))
                    raise NotImplementedError

        except (ConnectionClosed, TimeoutError) as exception:
            # XXX: LOG ?
            pass

        finally:
            if self.gameroom is not None:
                self.gameroom.remove_session(self)

    async def packet_handler(self, message: Message):
        if message.type is MessageType.ping:
            return

        raise NotImplementedError
