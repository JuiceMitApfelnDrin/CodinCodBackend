__all__ = ()

from typing import Final
from sanic import Sanic
from sanic.application.constants import ServerStage

app: Final = Sanic("CodinCod", log_config={"version": 1})
app.config.WEBSOCKET_MAX_SIZE = 128
app.config.WEBSOCKET_PING_INTERVAL = None  # type: ignore
app.config.WEBSOCKET_PING_TIMEOUT = None  # type: ignore
app.config.FALLBACK_ERROR_FORMAT = "json"

from .game_room import game_room_blueprint
from .puzzle import puzzle_blueprint
from .user import user_blueprint
from .app_ws import ws_blueprint
from .ide import ide_blueprint

app.blueprint([
    game_room_blueprint,
    puzzle_blueprint,
    user_blueprint,
    ws_blueprint,
    ide_blueprint
])

def app_start():
    if app.state.stage is not ServerStage.STOPPED:
        raise Exception("App is already running!")

    print("CodinCod is running on http://localhost:8080/")
    print("----------------------------------------------")

    app.run(host="0.0.0.0", port=8080, workers=1, debug=True, verbosity=1, access_log=False)