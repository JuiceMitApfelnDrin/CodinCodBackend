from __future__ import annotations

from sanic import text
from sanic.request import Request
from sanic.exceptions import SanicException

from .. import app
from ...exceptions import CodinCodException

@app.exception(CodinCodException)
def CodinCodg_error(request: Request, exception: CodinCodException):
    raise SanicException(exception.msg, status_code = exception.status)