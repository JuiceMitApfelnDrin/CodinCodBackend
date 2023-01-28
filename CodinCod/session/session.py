from __future__ import annotations
from dataclasses import dataclass, field

from sanic.server.websockets.impl import WebsocketImplProtocol
from websockets.exceptions import ConnectionClosed, ConnectionClosedError
from sanic.request import Request

from bson import ObjectId
import json

import asyncio
from typing import Final, ClassVar, Optional, TypedDict


from . import Message, SessionException
from ..user import User

@dataclass
class Session:
    timeout:    ClassVar[int] = 10  # secs
    __sessions: ClassVar[list[Session]] = []

    request: Request
    ws: WebsocketImplProtocol
    user: User = field(init = False)

    async def recv(self) -> Message:
        message = await self.ws.recv(self.timeout)
        if message is None:
            raise TimeoutError

        return Message.loads(message)

    async def send(self, message: Message):
        await self.ws.send(message.dumps())

    def __del__(self):
        self.__sessions.remove(self)
        self.user.release()
