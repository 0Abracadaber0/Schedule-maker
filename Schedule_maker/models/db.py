from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.pool import NullPool

from Schedule_maker.config import settings


class Database:
    def __init__(self, database_uri: str):
        self.engine = create_async_engine(
            database_uri,
            echo=True,
            poolclass=NullPool
        )
        self.async_session = async_sessionmaker(
            self.engine,
            class_=AsyncSession,
            expire_on_commit=False
        )

    async def get_db(self):
        async with self.async_session() as session:
            try:
                yield session
            finally:
                await session.close()


db = Database(settings.DATABASE_URI)

