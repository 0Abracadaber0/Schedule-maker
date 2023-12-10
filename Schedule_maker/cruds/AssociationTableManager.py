from typing import List
from abc import abstractmethod

from sqlalchemy import select, delete
from sqlalchemy.dialects.postgresql import insert
from starlette.exceptions import HTTPException
from starlette.status import HTTP_404_NOT_FOUND

from Schedule_maker.config.settings import Settings, settings
from Schedule_maker.models.db import Database, db
from Schedule_maker.models.core import classroom_subject_table
from Schedule_maker.security.PasswordManager import PasswordManager, password_manager
from Schedule_maker.models.core import Teacher, Subject, Classroom


class BaseAssociationTableManager:
    def __init__(self,
                 _db: Database,
                 _password_manager: PasswordManager,
                 _settings: Settings,
                 ):
        self.db = _db
        self.password_manager = _password_manager
        self.settings = _settings

    @abstractmethod
    async def create_association(self, *args, **kwargs):
        pass

    @abstractmethod
    async def delete_association(self, *args, **kwargs):
        pass


class SubjectClassroomAssociationManger(BaseAssociationTableManager):
    async def create_association(self, classroom_id, subject_id) -> None:
        async with db.engine.connect() as session:
            await session.execute(
                insert(classroom_subject_table).values(classroom_id=classroom_id, subject_id=subject_id)
            )
            await session.commit()

    async def delete_association(self, classroom_id, subject_id) -> None:
        async with db.engine.connect() as session:
            await session.execute(
                delete(classroom_subject_table).where(classroom_id=classroom_id, subject_id=subject_id)
            )
            await session.commit()

    async def get_association_by_classroom_id(self, classroom_id=None, subject_id=None):
        async with db.engine.connect() as session:
            coroutine_association = await session.execute(
                select(classroom_subject_table).where(classroom_id=classroom_id)
            )
            association = coroutine_association.first()
            if association is None:
                return None
            return association


subject_classroom_manager = SubjectClassroomAssociationManger(
    _db=db,
    _password_manager=password_manager,
    _settings=settings
)
