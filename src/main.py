from fastapi import FastAPI
from sqlalchemy.exc import OperationalError

from src.errors import operational_error_exc
from src.routers import user_router


def create_app():
    app = FastAPI()

    app.include_router(user_router.router)

    # add CORS
    # app.add_middleware(
    #    CORSMiddleware,
    #    allow_origins=["*"],
    #    allow_methods=["*"],
    #    allow_headers=["*"],
    # )

    @app.get("/")
    async def root():
        return {"message": "Online"}

    app.add_exception_handler(OperationalError, operational_error_exc)
    return app
