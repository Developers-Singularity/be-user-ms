from dotenv import load_dotenv
from fastapi import APIRouter, Depends

from src.database import db_session

router = APIRouter(prefix="/user", tags=["User"])

load_dotenv()


@router.get("/")
async def get_all_users(session=Depends(db_session)):
    print(session)
    return {"message": "returned"}
