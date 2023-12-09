from uuid import uuid4

from sqlalchemy import select, update, delete, insert

from starlette.exceptions import HTTPException
from starlette.status import HTTP_404_NOT_FOUND


from Schedule_maker.config.settings import Settings, settings
from Schedule_maker.models.core import Teacher
from Schedule_maker.models.db import Database, db
from Schedule_maker.security.PasswordManager import PasswordManager, password_manager


class TeacherManager:
    def __init__(self, _db: Database,
                 _password_manager: PasswordManager,
                 _settings: Settings
                 ):
        self.db = _db
        self.password_manager = password_manager
        self.settings = _settings

    async def get_teacher_by_id(self, _id: str) -> Teacher | None:
        async with self.db.engine.connect() as session:
            coroutine_teacher = await session.execute(select(Teacher).where(Teacher.id == _id))
        user = coroutine_teacher.first()
        if not user:
            return None
        return user

    async def delete_teacher_by_id(self, _id: str) -> None:
        teacher = await self.get_teacher_by_id(_id)
        if teacher:
            async with self.db.engine.connect() as session:
                await session.execute(delete(Teacher).where(Teacher.id == _id))
                await session.commit()
        else:
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND,
                detail="Teacher doesn't exist",
            )

    async def update_teacher(self, _id: str, teacher_full_name: str) -> None:
        teacher = await self.get_teacher_by_id(_id)
        if teacher:
            async with self.db.engine.connect() as session:
                session.execute(update(Teacher).where(Teacher.id == _id).values(full_name=teacher_full_name))
                await session.commit()
        else:
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND,
                detail="Teacher doesn't exist",
            )

    async def create_teacher(self, full_name: str, user_id: str) -> None:
        async with self.db.engine.connect() as session:
            await session.execute(insert(Teacher).values(full_name=full_name, user_id=user_id, id=str(uuid4())))
            await session.commit()


teacher_manager = TeacherManager(_db=db, _password_manager=password_manager, _settings=settings)
