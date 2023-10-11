from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session, async_session_maker
from src.users.crud import retrieve_user, add_user, get_users
from src.users.models import User
from src.users.schemas import UserResponse, PostUser, UserListResponse

router = APIRouter(
    prefix="/users",
    tags=['Users']
)


@router.get('/get/{user_id}/', response_model=UserResponse)
async def get_user(user_id: int, session: AsyncSession = Depends(get_async_session)):
    user = await retrieve_user(user_id, session)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user = user[0]
    return {
        "status": 200,
        "data": {
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "registered_at": user.registered_at
        },
        "message": "OK"
    }


@router.get('/list/', response_model=UserListResponse)
async def list_of_user(session: AsyncSession = Depends(get_async_session)):
    users = await get_users(session)
    return {
        "status": 200,
        "data": users,
        "message": "OK"
    }


@router.post('/create/', response_model=UserResponse)
async def create_user(user: PostUser):
    user = await add_user(user)
    if not user:
        raise HTTPException(status_code=404, detail="Bad request")
    return {
        "status": 200,
        "data": {
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "registered_at": user.registered_at
        },
        "message": "OK"
    }


@router.patch("/update/{user_id}")
async def update_user(user_id: int):
    pass
