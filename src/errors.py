"""
Module containing error handles for global handling
"""
import logging

from fastapi import Request
from sqlalchemy.exc import OperationalError, ProgrammingError
from starlette.responses import JSONResponse


class CustomException(Exception):
    def __init__(self, status_code: int, message: str, detail: str):
        self.status_code = status_code
        self.message = message
        self.detail = detail


def respond(status: int, detail: str, message: str):
    return JSONResponse(
        status_code=status,
        content={"status code": status, "message": message, "detail": detail},
    )


async def custom_exc(request: Request, error: CustomException):
    logging.error(f"{error.message}: {error.detail}")
    return respond(error.status_code, error.detail, error.message)


async def operational_error_exc(request: Request, error: OperationalError):
    if "Connection refused" in error.orig.__str__():
        logging.error(error.orig)
        return respond(503, str(type(error.orig)), str(error.orig))
    return respond(500, str(type(error.orig)), str(error.orig))


async def programming_error_exc(request: Request, error: ProgrammingError):
    logging.error(error.orig)
    return respond(503, str(type(error.orig)), str(error.orig))
