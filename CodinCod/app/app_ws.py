from sanic.server.websockets.impl import WebsocketImplProtocol
from sanic.request import Request
from . import app
from ..session.manager import SessionManager

app.config.WEBSOCKET_MAX_SIZE = 128
app.config.WEBSOCKET_PING_INTERVAL = None  # type: ignore
app.config.WEBSOCKET_PING_TIMEOUT = None  # type: ignore


@app.websocket("/", name='ws')
async def ws_handler(request: Request, ws: WebsocketImplProtocol):
    session = SessionManager(request, ws)
    await session.ws_handler()
