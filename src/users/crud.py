from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import async_session_maker
from users.models import User
from users.hashing import Hasher


async def get_users():
    async with async_session_maker() as session:
        async with session.begin():
            query = select(User)
            result = await session.execute(query)
            return result.all()


async def retrieve_user(pk: int, session: AsyncSession):
    stmt = select(User).filter(User.id == pk)
    result = await session.execute(stmt)
    return result.first()


async def add_user(user):
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
