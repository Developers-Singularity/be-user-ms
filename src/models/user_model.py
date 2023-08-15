"""
Module containing models for the user model
"""


from sqlalchemy import Column, Integer, String
from src.database import Base


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
