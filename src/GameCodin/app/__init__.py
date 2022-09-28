__all__ = ["app"]

from sanic.server.websockets.impl import WebsocketImplProtocol
from typing import Final
from sanic import Sanic
from sanic.application.state import ServerStage

app: Final = Sanic("GameCodin", log_config={"version": 1})

from . import app_ws
from . import app_routing

def start():
    if app.state.stage is not ServerStage.STOPPED:
        raise Exception("App is already running!")
    app.run(host="0.0.0.0", port=8080, workers=1, debug=False, access_log=False)