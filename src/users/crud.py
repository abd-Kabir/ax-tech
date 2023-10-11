from fastapi import HTTPException
from sqlalchemy import select, update, delete, text
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.database import async_session_maker
from src.users.models import User
from src.users.hashing import Hasher


async def get_users(search, session: AsyncSession):
    if search:
        query = select(User).where(text("LOWER(username) LIKE LOWER(:username)")).params(username=f"%{search}%")
    else:
        query = select(User)
    result = await session.execute(query)
    return result.scalars().all()


async def retrieve_user(user_id: int, session: AsyncSession):
    query = select(User).filter(User.id == user_id)
    result = await session.execute(query)
    user = result.first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user[0]


async def add_user(user):
    try:
        async with async_session_maker() as session:
            async with session.begin():
                hashed_password = Hasher.get_password_hash(user.password)
                new_user = User(
                    username=user.username,
                    hashed_password=hashed_password,
                    email=user.email
                )
                session.add(new_user)

            await session.commit()
            await session.refresh(new_user)
            return new_user
    except:
        raise HTTPException(detail="Email or Username like this already exists",
                            status_code=status.HTTP_400_BAD_REQUEST)


async def patch_user(user_id, data, session: AsyncSession):
    existing_user = await retrieve_user(user_id, session)

    data = data.non_none_dict()
    stmt = (
        update(User).
        where(User.id == user_id).
        values(**data)
    )
    await session.execute(stmt)
    await session.commit()
    return existing_user


async def delete_user(user_id, session: AsyncSession):
    stmt = (
        delete(User).
        where(User.id == user_id)
    )
    await session.execute(stmt)
    await session.commit()
    return user_id
