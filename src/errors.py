"""
Module containing error handles for global handling
"""
from fastapi import Request
from sqlalchemy.exc import OperationalError, ProgrammingError
from starlette.responses import JSONResponse


def respond(status: int, detail: str, message: str):
    return JSONResponse(
        status_code=503,
        content={"status code": status, "message": message, "detail": detail},
    )


async def operational_error_exc(request: Request, error: OperationalError):
    if "Connection refused" in error.orig.__str__():
        print(error.orig)
        return respond(503, str(type(error.orig)), str(error.orig))
    return respond(503, str(type(error.orig)), str(error.orig))


async def programming_error_exc(request: Request, error: ProgrammingError):
    return respond(503, str(type(error.orig)), str(error.orig))
