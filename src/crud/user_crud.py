import logging

from sqlalchemy.orm import Session

from src.errors import CustomException
from src.extensions import SecurityManager
from src.models.user_model import User
from src.schemas.user_schema import UserChangePassword, UserCreate


async def crud_create_user(session: Session, schema: UserCreate):
    # hashing password before save
    new_user = User(**schema.model_dump())
    new_user.password = SecurityManager.hash(hash_string=new_user.password)
    session.add(new_user)
    session.commit()
    return new_user


async def crud_change_password(session: Session, schema: UserChangePassword):
    if found := session.query(User).get(schema.id):
        if SecurityManager.compare_hash(found.password, schema.old_password):
            found.password = SecurityManager.hash(hash_string=schema.new_password)
            session.commit()
            return found
        else:
            raise CustomException(
                422,
                "Invalid password",
                "Old password does not match with the current one.",
            )
    raise CustomException(
        200, "Resource not found", f"User with ID {schema.id} not found"
    )


async def crud_get_all_users(session: Session):
    return session.query(User).all()


async def crud_get_user_by_id(session: Session, user_id: int):
    return session.query(User).get(user_id)
