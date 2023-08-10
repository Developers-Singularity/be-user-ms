"""
Module containing error handles for global handling
"""
from fastapi import Request
from sqlalchemy.exc import OperationalError
from starlette.responses import JSONResponse


async def operational_error_exc(request: Request, error: OperationalError):
    if "Connection refused" in error.orig.__str__():
        print("database is down")
        return JSONResponse(
            status_code=503,
            content={
                "status code": 503,
                "message": f"database is down",
                "error": f"{type(error)}"
            }
        )
    return JSONResponse(
        status_code=500,
        content={
            "status code": 500,
            "message": f"{str(error.orig)}",
            "error": f"{type(error)}"
        }
    )
