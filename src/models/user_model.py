import hashlib

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session

from src.database import Base
from src.extensions import SecurityManager


class User(Base):
    """
    User table, containing user information
    """

    __tablename__ = "user"

    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String(20), nullable=False, unique=True)
    password = Column(String(80), nullable=False)
    name = Column(String(20), nullable=True)
    surname = Column(String(20), nullable=True)
