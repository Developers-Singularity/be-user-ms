from fastapi import FastAPI
from sqlalchemy.exc import OperationalError, ProgrammingError
from fastapi.middleware.cors import CORSMiddleware
from src.errors import (
    operational_error_exc,
    programming_error_exc,
    custom_exc,
    CustomException,
)
from src.extensions import SecurityManager
from src.routers import user_router


def create_app():
    SecurityManager.validate_env()

    app = FastAPI()

    app.include_router(user_router.router)

    # add CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/")
    async def root():
        return {"message": "Online"}

    app.add_exception_handler(OperationalError, operational_error_exc)
    app.add_exception_handler(ProgrammingError, programming_error_exc)
    app.add_exception_handler(CustomException, custom_exc)

    return app
