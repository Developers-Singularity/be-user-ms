from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.database import db_session
from src.models.user_model import User
from src.schemas.user_schema import UserCreate, UserGet

router = APIRouter(prefix="/user", tags=["User"])


@router.post("/", response_model=UserGet, status_code=status.HTTP_201_CREATED)
async def crate_user(user_data: UserCreate, session: Session = Depends(db_session)):
    return await User(**user_data.model_dump()).create_user(session)


@router.get("/")
async def get_all_users(session=Depends(db_session)):
    print(session)
    return {"message": "returned"}
