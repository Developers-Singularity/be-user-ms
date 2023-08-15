"""
Module containing the routes authorization
"""
import logging

from fastapi import APIRouter


router = APIRouter(prefix="/auth", tags=["Authorization"])


@router.post("/login")
async def login():
    logging.info("REQUEST: login")
    # response = await crud_login(session, request_body)
    logging.info("Login successful.")
    return True  # response
