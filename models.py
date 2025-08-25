from typing import List
from beanie import Document, PydanticObjectId
from pydantic import BaseModel, EmailStr, Field


class User(Document):
    name: str 
    phone: int
    email: EmailStr = Field(...,unique = True)
    password: str
    role: str

class Create_user(BaseModel):
    name: str 
    phone: int
    email: EmailStr = Field(...,unique = True)
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
    vendor: str
    variant: List[Variants]

class AccessControl(Document):
    userid: str
    storeid: str
    accountid: str
    