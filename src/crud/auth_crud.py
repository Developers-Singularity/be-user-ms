from src.errors import CustomException
from src.extensions import SecurityManager
from src.schemas.auth_schema import LoginSchema
from src.models.user_model import User
from sqlalchemy.orm import Session

from src.schemas.user_schema import UserGet


async def crud_login(session: Session, schema: LoginSchema):
    """CRUD function to login

    Args:
        session (Session): database session
        request_body (LoginSchema): schema containing data

    Returns:
        User: User object which was updated
    """
    if found := session.query(User).filter_by(email=schema.email).first():
        if SecurityManager.compare_hash(found.password, schema.password):
            return {
                "token": SecurityManager.generate_jwt(
                    UserGet.model_validate(found).model_dump()
                ),
                "token_type": "bearer",
            }
        else:
            raise CustomException(
                422,
                "Invalid password",
                "Old password does not match with the current one.",
            )
    raise CustomException(
        200, "Resource not found", f"User with email {schema.email} not found."
    )
