import uuid

from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import RedirectResponse

from sqlalchemy import select
from sqlalchemy.orm import Session

from typing import Annotated

from starlette import status
from starlette.exceptions import HTTPException
from starlette.status import HTTP_403_FORBIDDEN

from Schedule_maker.config import settings
from Schedule_maker.models.db import db
from Schedule_maker.models.core import Teacher, User
from Schedule_maker.cruds.UserManager import user_manager
from Schedule_maker.cruds.TeacherManager import teacher_manager


router = APIRouter()


@router.get('/teacher')
async def teacher_table(
        request: Request,
        current_user: Annotated[User, Depends(user_manager.get_current_verified_user)],
        db_: Session = Depends(db.get_db)
):
    coroutine_teachers = await db_.execute(select(Teacher).where(Teacher.user_id == current_user.id))
    teachers = coroutine_teachers.scalars()
    return settings.templates.TemplateResponse(
        'teacher_table.html',
        {
            'request': request,
            'teachers': teachers
        }
    )


@router.post('/teacher')
async def teacher_table(
        current_user: Annotated[User, Depends(user_manager.get_current_verified_user)],
        full_name: str = Form(),
):
    user = await user_manager.get_user_by_id(current_user.id)
    await teacher_manager.create_teacher(full_name, user.id)
    response = RedirectResponse('/tables/teacher')
    response.status_code = 302
    return response


@router.get('/teacher-delete/{teacher_id}')
async def teacher_table(
        current_user: Annotated[User, Depends(user_manager.get_current_verified_user)],
        teacher_id: str
):
    teacher = await teacher_manager.get_teacher_by_id(teacher_id)
    if teacher.user_id == current_user.id:
        await teacher_manager.delete_teacher_by_id(teacher_id)
        return RedirectResponse('/tables/teacher')
    raise HTTPException(
        status_code=HTTP_403_FORBIDDEN,
        detail='You do not have permission to delete this teacher'
    )


@router.get('/teacher-delete/{teacher_id}/{new_full_name}')
async def teacher_table(
        current_user: Annotated[User, Depends(user_manager.get_current_verified_user)],
        teacher_id: str,
        new_full_name: str
):
    teacher = teacher_manager.get_teacher(teacher_id)
    if teacher.user_id == current_user.id:
        teacher_manager.update_teacher(teacher_id, new_full_name)
        return RedirectResponse('/tables/teacher', status_code=status.HTTP_303_SEE_OTHER)
    raise HTTPException(
        status_code=HTTP_403_FORBIDDEN,
        detail='You do not have permission to change data about this teacher'
    )
