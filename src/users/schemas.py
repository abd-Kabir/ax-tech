from datetime import datetime

from pydantic import BaseModel


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
