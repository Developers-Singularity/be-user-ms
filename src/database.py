"""
Python Module for Handling Database connection via SQLAlchemy.
"""
import os

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from src.extensions import env_values


engine = create_engine(env_values["DB_URI"], pool_size=0, max_overflow=-1)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def db_session():
    """
    Function to yield Database Session instance.
    :return:
    """
    session = SessionLocal()
    try:
        session.execute(text("SELECT 1"))
        yield session
    finally:
        session.close()