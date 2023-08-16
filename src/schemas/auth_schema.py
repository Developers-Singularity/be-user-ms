from pydantic import BaseModel, ConfigDict, EmailStr, constr


class LoginSchema(BaseModel):
    """Schema for login"""
    
    email: EmailStr
    password: constr(min_length=4, max_length=20)

class LoginResponse(BaseModel):
    """Schema to return token and token type"""
    
    token: str
    token_type: str
class AuthSchema(BaseModel):
    """Schema for token validation"""
    
    token: str