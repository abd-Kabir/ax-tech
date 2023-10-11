from datetime import datetime
from typing import List, Optional

from fastapi_users import schemas
from pydantic import BaseModel


# FastAPI-users

class UserRead(schemas.BaseUser[int]):
    id: int
    username: str
    email: str
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False

    class Config:
        orm_mode = True


class UserCreate(schemas.BaseUserCreate):
    username: str
    email: str
    password: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False


# Serializers
class PostUser(BaseModel):
    email: str
    username: str
    password: str


class PatchUser(BaseModel):
    email: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None

    def non_none_dict(self):
        return {k: v for k, v in self.dict().items() if v is not None}


# ResponseModels
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
    data: List[UserData]
    message: str
