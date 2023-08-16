"""
Module containing the routes authorization
"""
import logging

from fastapi import APIRouter, Depends, status
from src.database import db_session
from src.crud.auth_crud import crud_login
from sqlalchemy.orm import Session
from src.extensions import SecurityManager
from src.schemas.auth_schema import TokenSchema, LoginSchema


router = APIRouter(prefix="/auth", tags=["Authorization"])


@router.post("/login",response_model=TokenSchema, status_code=status.HTTP_200_OK)
async def login(request_body: LoginSchema, session: Session = Depends(db_session)):
    logging.info("REQUEST: login")
    response = await crud_login(session, request_body)
    logging.info("Login successful.")
    return response

@router.post("/",status_code=status.HTTP_200_OK)
async def authenticate(request_body: TokenSchema):
    logging.info("REQUEST: authenticate")
    response = await SecurityManager.authenticate(request_body.model_dump()["token"])
    logging.info("Authentication successful.")
    return response