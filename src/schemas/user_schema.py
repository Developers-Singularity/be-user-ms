from pydantic import BaseModel, constr


class UserGet(BaseModel):
    id: int
    username: str
    name: str
    surname: str

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    """
    Schema when creating user
    """

    username: constr(min_length=4, max_length=20)
    password: constr(min_length=4, max_length=20)
    name: constr(min_length=4, max_length=20)
    surname: constr(min_length=4, max_length=20)


class UserChangePassword(BaseModel):
    id: int
    old_password: str
    new_password: constr(min_length=4, max_length=20)


class UserUpdate(BaseModel):
    name: constr(min_length=4, max_length=20) | None = None
    surname: constr(min_length=4, max_length=20) | None = None
