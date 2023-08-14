import logging

from sqlalchemy.orm import Session

from src.errors import CustomException
from src.extensions import SecurityManager
from src.models.user_model import User
from src.schemas.user_schema import UserChangePassword, UserCreate


async def crud_create_user(session: Session, schema: UserCreate):
    """CRUD function to create new User

    :param session: database session
    :type session: Session
    :param schema: schema containing data
    :type schema: UserCreate
    :return: Created user
    :rtype: User
    """
    # hashing password before save
    new_user = User(**schema.model_dump())
    new_user.password = SecurityManager.hash(hash_string=new_user.password)
    session.add(new_user)
    session.commit()
    return new_user


async def crud_change_password(session: Session, schema: UserChangePassword):
    """_summary_

    :param session: database session
    :type session: Session
    :param schema: schema containing data
    :type schema: UserChangePassword
    :raises CustomException: Handled exception: Invalid password
    :raises CustomException: Handled exception: User not found
    :return: User object which password was changed
    :rtype: User
    """
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
        200, "Resource not found", f"User with ID {schema.id} not found."
    )


async def crud_get_all_users(session: Session):
    """CRUD function to get all User data

    :param session: database session
    :type session: Session
    :return: Found users
    :rtype: List[User]
    """
    return session.query(User).all()


async def crud_get_user_by_id(session: Session, user_id: int):
    """CRUD function to get User data by ID

    :param session: database session
    :type session: Session
    :param user_id: ID of user to find
    :type user_id: int
    :raises CustomException: Handled exception: User not found
    :return: Found user
    :rtype: User
    """
    if response := session.query(User).get(user_id):
        return response
    raise CustomException(
        200, "Resource not found", f"User with ID:{user_id} not found."
    )
