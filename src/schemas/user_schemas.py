from typing import Optional
from pydantic import BaseModel, EmailStr, Field, HttpUrl
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4
from src.database.models import Role


class UserModel(BaseModel):
    user_role: Role = 'client'
    password: str = Field(min_length=8)
    name: str = Field(min_length=5, max_length=30)
    email: EmailStr
    phone: str
    avatar: Optional[str] = Field(None)


class UserResponse(BaseModel):
    user_id: int = Field(default_factory=lambda: uuid4().hex)
    user_role: Role = 'client'
    password: str = Field(min_length=6)
    name: str = "Oksana"
    email: EmailStr = "oksana@gmail.com"
    phone: str
    avatar: Optional[str] = Field(None)

    class Config:
        from_attributes = True


class AdminModel(UserModel):
    user_id: int = Field(default_factory=lambda: uuid4().hex)
    user_role: Role = 'admin'
    is_active: bool = True


class AdminResponse(UserResponse):
    admin_id: int = Field(default_factory=lambda: uuid4().hex)
    user_role: Role = 'admin'
    is_active: bool

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    name: str
    email: EmailStr


class UserBlackList(BaseModel):
    banned: Optional[bool] = False

    class Config:
        from_attributes = True


class UserBlacklistResponse(BaseModel):
    user_id: int = Field(default_factory=lambda: uuid4().hex)
    name: str = "Oksana"
    email: EmailStr = "oksana@gmail.com"
    role: Role = "client"
    banned: Optional[bool] = False

    class Config:
        from_attributes = True
