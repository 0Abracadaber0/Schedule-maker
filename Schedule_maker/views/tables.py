from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import RedirectResponse

from sqlalchemy import select
from sqlalchemy.orm import Session

from typing import Annotated

from Schedule_maker.config import settings
from Schedule_maker.models.db import db
from Schedule_maker.models.core import Teacher, User, generate_uuid
from Schedule_maker.models.UserManager import user_manager


router = APIRouter()


@router.get('/teacher')
async def teacher_table(
        request: Request,
        current_user: Annotated[User, Depends(user_manager.get_current_verified_user)],
        db_: Session = Depends(db.get_db)
):
    coroutine_teachers = await db_.execute(select(Teacher).where(Teacher.user_id == current_user.id))
    teachers = coroutine_teachers.scalars()
    print(teachers)
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
        db_: Session = Depends(db.get_db)
):
    user = await user_manager.get_user_by_id(current_user.id)
    teacher = Teacher(
        user_id=user.id,
        full_name=full_name
    )
    teacher.id = generate_uuid()
    db_.add(teacher)
    await db_.commit()
    return RedirectResponse('/teacher')
