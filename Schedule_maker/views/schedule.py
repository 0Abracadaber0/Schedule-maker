import uuid
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse

from Schedule_maker.cruds.TableObjectManager import schedule_manager
from Schedule_maker.cruds.UserManager import user_manager
from Schedule_maker.models.core import User
from Schedule_maker.models.db import db
from controller.main import ScheduleGenerator
from controller.serializer.Serializer import Serializer

router = APIRouter()


class ScheduleView:
    @staticmethod
    @router.get("/download")
    async def download(
            current_user: Annotated[User, Depends(user_manager.get_current_verified_user)]
    ):
        serializer = Serializer(
            _db=db,
            user_id=current_user.id
        )
        schedule_generator = ScheduleGenerator(
            await serializer.get_subject(),
            await serializer.get_group(),
            await serializer.get_curriculum(),
            await serializer.get_classroom()
        )
        current_schedule_id = str(uuid.uuid4())
        await schedule_manager.create_object(
            {
                'user_id': current_user.id,
                'id': current_schedule_id
            }
        )
        schedule_generator.main(

            path=f'/home/ubuntu/Schedule-maker/controller/schedules/{current_schedule_id}.xlsx'
        )
        return FileResponse(
            f'/home/ubuntu/Schedule-maker/controller/schedules/{current_schedule_id}.xlsx'
        )
