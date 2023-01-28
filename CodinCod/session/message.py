from __future__ import annotations

from dataclasses import dataclass
import json

from . import MessageType
from .expection import InvalidMessageException


@dataclass
class Message:
    type: MessageType
    content: object
    
    def dumps(self):
        return json.dumps({
            "type": self.type.value,
            "content": self.content
        })

    @classmethod
    def loads(cls, message: str | bytes):
        try:
            message_dict = json.loads(message)
        except ValueError:
            message_dict = None

        if not type(message_dict) is dict or\
            message_dict.keys() != {"type", "content"} or\
            message_dict["type"] not in MessageType:
            raise InvalidMessageException("Recieved an Invalid message {message}")

        return Message(
            MessageType[message_dict["type"]],
            message_dict["content"])

        