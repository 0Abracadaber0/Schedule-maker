from asyncio import run
from sqlalchemy import select


from Schedule_maker.config.settings import Settings, settings
from Schedule_maker.models.db import Database, db
from Schedule_maker.security.PasswordManager import PasswordManager, password_manager
from Schedule_maker.models.core import Group, Curriculum


class Serializer:
    def __init__(self,
                 _db: Database,
                 _password_manager: PasswordManager,
                 _settings: Settings,
                 user_id: str
                 ):
        self.db = _db
        self.password_manager = _password_manager
        self.settings = _settings
        self.user_id = user_id

    async def get_group(self):
        async with self.db.engine.begin() as session:
            coroutine_groups = await session.execute(
                select(Group).where(Group.user_id == self.user_id)
            )
            groups = coroutine_groups.fetchall()
            groups_curriculums = {}
            for group in groups:
                coroutine_curriculum = await session.execute(
                    select(Curriculum).where(Curriculum.id == group.curriculum_id)
                )
                curriculum = coroutine_curriculum.fetchone()
                groups_curriculums.update(
                    {
                        group.group_name:
                        curriculum.name
                    }
                )
            return groups_curriculums

    async def get_curriculum(self):
        async with self.db.engine.begin() as session:
            coroutine_curriculums = await session.execute(
                select(Curriculum).where(Curriculum.user_id == self.user_id)
            )
            curriculums = coroutine_curriculums.fetchall()





serializer = Serializer(
    _db=db,
    _settings=settings,
    _password_manager=password_manager,
    user_id="f672a27b-1e86-4dc8-b0a9-e0b6c1680c18"
)

run(serializer.get_curriculum())
