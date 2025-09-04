from typing import List, Optional
from beanie import Document, PydanticObjectId
from pydantic import BaseModel, EmailStr, Field


class User(Document):
    name: str 
    phone: int
    email: EmailStr = Field(...,unique = True)
    password: str
    role: str

class CreateUser(BaseModel):
    name: str 
    phone: int
    email: EmailStr
    password: str
    role: str

class SigninPayload(BaseModel):
    email: EmailStr
    password: str

class Variants(BaseModel):
    id: PydanticObjectId = None
    title: str = "Default Variant Title"
    price: int
    stock: int

class Products(Document):
    title: str
    vendor: Optional[str] = None
    variant: List[Variants]

class AccessControl(Document):
    userid: PydanticObjectId
    storeid: Optional[PydanticObjectId] = None
    accountid: Optional[PydanticObjectId] = None

    