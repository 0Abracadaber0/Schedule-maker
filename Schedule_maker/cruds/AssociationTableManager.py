from abc import abstractmethod

from sqlalchemy import select, delete
from sqlalchemy.dialects.postgresql import insert

from Schedule_maker.config.settings import Settings, settings
from Schedule_maker.models.db import Database, db
from Schedule_maker.models.core import ClassroomSubject, Classroom, Subject
from Schedule_maker.security.PasswordManager import PasswordManager, password_manager
from Schedule_maker.cruds.TableObjectManager import classroom_manager, subject_manager


class BaseAssociationTableManager:
    def __init__(self,
                 _db: Database,
                 _password_manager: PasswordManager,
                 _settings: Settings,
                 association_object
                 ):
        self.db = _db
        self.password_manager = _password_manager
        self.settings = _settings
        self.association_object = association_object

    @abstractmethod
    async def create_association(self, *args, **kwargs):
        pass

    @abstractmethod
    async def delete_association(self, *args, **kwargs):
        pass


class SubjectClassroomAssociationManger(BaseAssociationTableManager):
    async def create_association(self, classroom_id: str, subject_id: str, user_id: str, _id: str) -> None:
        async with db.engine.connect() as session:
            await session.execute(
                insert(self.association_object).values(
                    classroom_id=classroom_id,
                    subject_id=subject_id,
                    user_id=user_id,
                    id=_id
                )
            )
            await session.commit()

    async def delete_association(self, classroom_id: str, subject_id: str) -> None:
        async with db.engine.connect() as session:
            await session.execute(
                delete(self.association_object).where(
                    self.association_object.classroom_id == classroom_id,
                    self.association_object.subject_id == subject_id
                )
            )
            await session.commit()

    async def get_all_associations_by_user_id(self, user_id: str):
        async with self.db.engine.connect() as session:
            coroutine_association = await session.execute(
                select(self.association_object).where(self.association_object.user_id == user_id)
            )
            associations = coroutine_association.fetchall()
            if associations is None:
                return None
            subject_classroom_dict = {}
            for association in associations:
                subject_classroom_dict.update(
                    {
                        await subject_manager.get_object_by_id(association.subject_id):
                        await classroom_manager.get_object_by_id(association.classroom_id)
                    }
                )
            return subject_classroom_dict


subject_classroom_manager = SubjectClassroomAssociationManger(
    _db=db,
    _password_manager=password_manager,
    _settings=settings,
    association_object=ClassroomSubject
)
