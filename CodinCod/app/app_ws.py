from sanic.server.websockets.impl import WebsocketImplProtocol
from sanic.request import Request
from sanic import Blueprint

from typing import Final

from ..session.manager import SessionManager

ws_blueprint: Final = Blueprint('ws', url_prefix='/')

@ws_blueprint.websocket("/", name='ws')
async def ws_handler(request: Request, ws: WebsocketImplProtocol):
    session = SessionManager(request, ws)
    await session.ws_handler()
