from typing import List

from sqlalchemy import select, delete
from sqlalchemy.dialects.postgresql import insert
from starlette.exceptions import HTTPException
from starlette.status import HTTP_404_NOT_FOUND

from Schedule_maker.models.db import Database, db
from Schedule_maker.models.core import Teacher, Subject, Classroom, Curriculum, Group, Schedule


class TableObjectManager:
    def __init__(self,
                 _db: Database,
                 table_object
                 ):
        self.db = _db
        self.table_object = table_object

    async def get_object_by_id(self, _id: str) -> object | None:
        async with self.db.engine.connect() as session:
            coroutine_table_object = await session.execute(select(self.table_object).filter(
                self.table_object.id == _id)
            )
        table_object = coroutine_table_object.fetchone()
        if not table_object:
            return None
        return table_object

    async def delete_object_by_id(self, _id: str) -> None:
        table_object = await self.get_object_by_id(_id)
        if table_object:
            async with self.db.engine.connect() as session:
                await session.execute(delete(self.table_object).where(self.table_object.id == _id))
                await session.commit()
        else:
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND,
                detail=f"{type(self.table_object)} object doesn't exist",
            )

    async def create_object(self, params: dict) -> None:
        async with self.db.engine.connect() as session:
            await session.execute(insert(self.table_object).values(**params))
            await session.commit()

    async def get_all_objects_by_user_id(self, user_id: str) -> List[object]:
        async with self.db.engine.connect() as session:
            coroutine_table_objects = await session.execute(
                select(self.table_object).where(self.table_object.user_id == user_id)
            )
            table_objects = coroutine_table_objects.all()
            return table_objects


class CurriculumTableManager(TableObjectManager):
    async def get_object_by_name(self, name: str):
        async with self.db.engine.connect() as session:
            coroutine_group = await session.execute(
                select(self.table_object).where(self.table_object.name == name)
            )
            group = coroutine_group.fetchone()
            if group:
                return group
            return None


teacher_manager = TableObjectManager(
    _db=db,
    table_object=Teacher
)

subject_manager = TableObjectManager(
    _db=db,
    table_object=Subject
)

classroom_manager = TableObjectManager(
    _db=db,
    table_object=Classroom
)

curriculum_manager = CurriculumTableManager(
    _db=db,
    table_object=Curriculum
)

group_manager = TableObjectManager(
    _db=db,
    table_object=Group
)

schedule_manager = TableObjectManager(
    _db=db,
    table_object=Schedule
)
