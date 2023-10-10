from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import async_session_maker
from src.users.models import User
from src.users.hashing import Hasher


async def get_users(session: AsyncSession):
    query = select(User)
    result = await session.execute(query)
    return result.scalars().all()


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
