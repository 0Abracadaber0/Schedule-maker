from sqlalchemy import (
    select
)
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
)
from dotenv import (
    load_dotenv
)
from os import (
    getenv
)
from fastapi import (
    Depends
)
from fastapi_users.db import (
    SQLAlchemyUserDatabase,
)
from fastapi_users import (
    models,
)


from .core import (
    User
)

load_dotenv()


DATABASE_URL = getenv('DATABASE_URL')

engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


async def get_db():
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()


async def get_user_db(session: AsyncSession = Depends(get_db)):
    yield SQLAlchemyUserDatabase(session, User)


async def db_get_by_username(username: str) -> models.UP:
    async with async_session_maker() as session:
        user = await session.execute(select(User).where(User.username == username))
    return user.scalar()
