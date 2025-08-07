from pydantic import BaseModel, EmailStr


class UserResponse(BaseModel):
    _id: str
    name: str 
    phone: int
    email: EmailStr 
    role: str

class AuthResponse(BaseModel):
    token: str
    user: UserResponse
