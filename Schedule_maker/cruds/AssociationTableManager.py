from abc import abstractmethod

from sqlalchemy import select, delete
from sqlalchemy.dialects.postgresql import insert

from Schedule_maker.config.settings import Settings, settings
from Schedule_maker.models.db import Database, db
from Schedule_maker.models.core import ClassroomSubject, SubjectTeacher, CurriculumSubject
from Schedule_maker.security.PasswordManager import PasswordManager, password_manager
from Schedule_maker.cruds.TableObjectManager import (
    classroom_manager, subject_manager, teacher_manager, curriculum_manager
)


class BaseAssociationTableManager:
    def __init__(self,
                 _db: Database,
                 _password_manager: PasswordManager,
                 _settings: Settings,
                 association_object,
                 first_manger,
                 second_manger
                 ):
        self.db = _db
        self.password_manager = _password_manager
        self.settings = _settings
        self.association_object = association_object
        self.first_manger = first_manger
        self.second_manger = second_manger

    @abstractmethod
    async def create_association(self, *args, **kwargs):
        pass

    @abstractmethod
    async def delete_association(self, *args, **kwargs):
        pass

    async def get_all_associations_by_user_id(self, user_id: str):
        async with self.db.engine.connect() as session:
            coroutine_association = await session.execute(
                select(self.association_object).where(self.association_object.user_id == user_id)
            )
            associations = coroutine_association.fetchall()
            if associations is None:
                return None
            subject_teacher_dict = {}
            for association in associations:
                subject_teacher_dict.update(
                    {
                        await self.first_manger.get_object_by_id(association.subject_id):
                        await self.second_manger.get_object_by_id(association.teacher_id)
                    }
                )
            return subject_teacher_dict


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
            associations = coroutine_association.all()
            if associations is None:
                return None
            subject_classroom_dict = []
            for association in associations:
                subject_classroom_dict.append(
                    [
                        await self.first_manger.get_object_by_id(association.subject_id),
                        await self.second_manger.get_object_by_id(association.classroom_id)
                    ]
                )
            return subject_classroom_dict


class SubjectTeacherAssociationManager(BaseAssociationTableManager):
    async def create_association(self, teacher_id: str, subject_id: str, user_id: str, _id: str) -> None:
        async with self.db.engine.connect() as session:
            await session.execute(
                insert(self.association_object).values(
                    teacher_id=teacher_id,
                    subject_id=subject_id,
                    user_id=user_id,
                    id=_id
                )
            )
            await session.commit()

    async def delete_association(self, teacher_id: str, subject_id: str) -> None:
        async with db.engine.connect() as session:
            await session.execute(
                delete(self.association_object).where(
                    self.association_object.teacher_id == teacher_id,
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
            subject_teacher_dict = []
            for association in associations:
                subject_teacher_dict.append(
                    [
                        await self.first_manger.get_object_by_id(association.subject_id),
                        await self.second_manger.get_object_by_id(association.teacher_id)
                    ]
                )
            return subject_teacher_dict


class SubjectCurriculumAssociationManager(BaseAssociationTableManager):
    async def create_association(self, curriculum_id: str, subject_id: str, user_id: str, _id: str) -> None:
        async with self.db.engine.connect() as session:
            await session.execute(
                insert(self.association_object).values(
                    curriculum_id=curriculum_id,
                    subject_id=subject_id,
                    user_id=user_id,
                    id=_id
                )
            )
            await session.commit()

    async def delete_association(self, curriculum_id: str, subject_id: str) -> None:
        async with db.engine.connect() as session:
            await session.execute(
                delete(self.association_object).where(
                    self.association_object.curriculum_id == curriculum_id,
                    self.association_object.subject_id == subject_id
                )
            )
            await session.commit()

    async def get_all_associations_by_user_id(self, user_id: str):
        async with self.db.engine.connect() as session:
            coroutine_association = await session.execute(
                select(self.association_object).where(self.association_object.user_id == user_id)
            )
            associations = coroutine_association.all()
            if associations is None:
                return None
            curriculum_teacher_dict = []
            for association in associations:
                curriculum_teacher_dict.append(
                    [
                        await self.first_manger.get_object_by_id(association.subject_id),
                        await self.second_manger.get_object_by_id(association.curriculum_id)
                    ]
                )
            return curriculum_teacher_dict


subject_classroom_manager = SubjectClassroomAssociationManger(
    _db=db,
    _password_manager=password_manager,
    _settings=settings,
    association_object=ClassroomSubject,
    first_manger=subject_manager,
    second_manger=classroom_manager
)

subject_teacher_manager = SubjectTeacherAssociationManager(
    _db=db,
    _password_manager=password_manager,
    _settings=settings,
    association_object=SubjectTeacher,
    first_manger=subject_manager,
    second_manger=teacher_manager
)

subject_curriculum_manager = SubjectCurriculumAssociationManager(
    _db=db,
    _password_manager=password_manager,
    _settings=settings,
    association_object=CurriculumSubject,
    first_manger=subject_manager,
    second_manger=curriculum_manager
)
