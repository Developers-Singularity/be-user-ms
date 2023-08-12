import logging

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.crud.user_crud import create_user, change_password
from src.database import db_session
from src.schemas.user_schema import UserCreate, UserGet, UserChangePassword

router = APIRouter(prefix="/user", tags=["User"])


@router.post("/", response_model=UserGet, status_code=status.HTTP_201_CREATED)
async def crate_user(request_body: UserCreate, session: Session = Depends(db_session)):
    logging.info("REQUEST: create user")
    response = await create_user(session, request_body)
    logging.info("User created successfully.")
    return response


@router.patch("/change-password", response_model=UserGet, status_code=status.HTTP_200_OK)
async def patch_password(request_body: UserChangePassword, session: Session = Depends(db_session)):
    logging.info("REQUEST: change password")
    response = await change_password(session, request_body)
    logging.info("Password changed successfully.")
    return response


@router.get("/")
async def get_all_users(session=Depends(db_session)):
    print(session)
    return {"message": "returned"}
