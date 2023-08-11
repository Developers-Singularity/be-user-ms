from pydantic import BaseModel, constr


class UserGet(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    """
    Schema when creating user
    """

    username: constr(min_length=4, max_length=20)
    password: constr(min_length=4, max_length=20)

    class Config:
        from_attributes = True
