from datetime import datetime
from typing import List

from pydantic import BaseModel

from src.users.models import User


class PostUser(BaseModel):
    email: str
    username: str
    password: str


class UserData(BaseModel):
    id: int
    email: str
    username: str
    registered_at: datetime


class UserResponse(BaseModel):
    status: int
    data: UserData
    message: str


class UserListResponse(BaseModel):
    status: int
    data: List[User]
    message: str

    class Config:
        arbitrary_types_allowed = True
