# schemas.py
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
    name: str
    email: EmailStr
    password: str

    class Config:
        from_attributes = True


class AddUserToDb(BaseModel):
    name: str
    email: EmailStr
    hashed_password: str
    is_activated: bool

    class Config:
        from_attributes = True


class UserRegistrationResponse(BaseModel):
    is_activated: bool
    name: str

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str


class UserLogin(BaseModel):
    username: str
    password: str


class CreateItem(BaseModel):
    title: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    status: bool
    # owner: int

    class Config:
        from_attributes = True


class Item(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    status: bool
    owner_id: int
    created_date: datetime

    class Config:
        from_attributes = True





class UpdateItem(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[datetime] = None

    class Config:
        from_attributes = True
