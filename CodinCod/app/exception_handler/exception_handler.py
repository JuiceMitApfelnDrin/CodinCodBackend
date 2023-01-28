from __future__ import annotations

from sanic import text, json
from sanic.response import HTTPResponse
from sanic.request import Request

from bson.objectid import ObjectId
from bson.errors import InvalidId

from .. import app

from ...exceptions import CodinCodException


@app.exception(CodinCodException)
def CodinCodg_error(request: Request, exception: CodinCodException):
    return text(exception.msg, status = exception.status)


# disabled for debugging purposes for now
# TODO: add an option to enable debugging for both types of exceptions
"""
@app.exception(Exception)
def internal_error(request: Request, exception: Exception):
    return text("Internal Error" + str(exception), status = 400)
"""