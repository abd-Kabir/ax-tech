import logging

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.database import get_async_session
from src.users.crud import retrieve_user, add_user, get_users, patch_user, delete_user
from src.users.schemas import UserResponse, PostUser, UserListResponse, PatchUser

router = APIRouter(
    prefix="/users",
    tags=['Users']
)


@router.get('/get/{user_id}/', response_model=UserResponse)
async def get_user(user_id: int, session: AsyncSession = Depends(get_async_session)):
    try:
        user = await retrieve_user(user_id, session)
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
    except Exception as exc:
        logging.error(f'exception: {exc.args}')
        raise HTTPException(detail='Bad request', status_code=status.HTTP_400_BAD_REQUEST)


@router.get('/list/', response_model=UserListResponse)
async def list_of_user(
        search: str = Query(None, title="Username to search for"),
        sort_by: str = Query(None, title="Field to sort by (id or username)"),
        sort_order: str = Query(None, title="Sort order (asc or desc)"),
        session: AsyncSession = Depends(get_async_session)
):
    try:
        users = await get_users(search, session)
        if sort_by == "username":
            users = sorted(users, key=lambda user: user.username)
        else:
            users = sorted(users, key=lambda user: user.id)

        if sort_order == "desc":
            users = list(reversed(users))

        return {
            "status": 200,
            "data": users,
            "message": "OK"
        }
    except Exception as exc:
        logging.error(f'exception: {exc.args}')
        raise HTTPException(detail='Bad request', status_code=status.HTTP_400_BAD_REQUEST)


@router.post('/create/', response_model=UserResponse)
async def create_user(user: PostUser):
    try:
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
    except Exception as exc:
        logging.error(f'exception: {exc.args}')
        raise HTTPException(detail='Bad request', status_code=status.HTTP_400_BAD_REQUEST)


@router.patch("/update/{user_id}/", response_model=UserResponse)
async def update_user(user_id: int, data: PatchUser, session: AsyncSession = Depends(get_async_session)):
    try:
        updated_user = await patch_user(user_id, data, session)
        if not updated_user:
            raise HTTPException(status_code=404, detail="Bad request")
        return {
            "status": 200,
            "data": {
                "id": updated_user.id,
                "email": updated_user.email,
                "username": updated_user.username,
                "registered_at": updated_user.registered_at
            },
            "message": "OK"
        }
    except Exception as exc:
        logging.error(f'exception: {exc.args}')
        raise HTTPException(detail='Bad request', status_code=status.HTTP_400_BAD_REQUEST)


@router.delete("/delete/{user_id}/")
async def destroy_user(user_id: int, session: AsyncSession = Depends(get_async_session)):
    try:
        await delete_user(user_id, session)
        return
    except Exception as exc:
        logging.error(f'exception: {exc.args}')
        raise HTTPException(detail='Bad request', status_code=status.HTTP_400_BAD_REQUEST)
