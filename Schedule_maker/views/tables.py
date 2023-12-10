import uuid

from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import RedirectResponse

from typing import Annotated

from starlette import status
from starlette.exceptions import HTTPException
from starlette.status import HTTP_403_FORBIDDEN

from Schedule_maker.config import settings
from Schedule_maker.models.core import User
from Schedule_maker.cruds.UserManager import user_manager
from Schedule_maker.cruds.AssociationTableManager import subject_classroom_manager
from Schedule_maker.cruds.TableObjectManager import teacher_manager, subject_manager, classroom_manager


router = APIRouter()


class TeacherTable:
    @staticmethod
    @router.get('/teacher')
    async def teacher_table(
            request: Request,
            current_user: Annotated[User, Depends(user_manager.get_current_verified_user)],
    ):
        teachers = await teacher_manager.get_all_objects_by_user_id(current_user.id)
        return settings.templates.TemplateResponse(
            'teacher_table.html',
            {
                'request': request,
                'teachers': teachers
            }
        )

    @staticmethod
    @router.post('/teacher')
    async def teacher_table(
            current_user: Annotated[User, Depends(user_manager.get_current_verified_user)],
            full_name: str = Form(),
    ):
        user = await user_manager.get_user_by_id(current_user.id)
        await teacher_manager.create_object(
            {
                'full_name': full_name,
                'user_id': user.id,
                'id': str(uuid.uuid4())
            }
        )
        response = RedirectResponse('/tables/teacher')
        response.status_code = 302
        return response

    @staticmethod
    @router.get('/teacher-delete/{teacher_id}')
    async def teacher_table(
            current_user: Annotated[User, Depends(user_manager.get_current_verified_user)],
            teacher_id: str
    ):
        teacher = await teacher_manager.get_object_by_id(teacher_id)
        if teacher.user_id == current_user.id:
            await teacher_manager.delete_object_by_id(teacher_id)
            return RedirectResponse('/tables/teacher')
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail='You do not have permission to delete this teacher'
        )


class SubjectsTableView:
    @staticmethod
    @router.get('/subject')
    async def subject_table(
            request: Request,
            current_user: Annotated[User, Depends(user_manager.get_current_verified_user)]
    ):
        subjects = await subject_manager.get_all_objects_by_user_id(current_user.id)
        return settings.templates.TemplateResponse('subject_table.html', {
            'request': request,
            'subjects': subjects
        })

    @staticmethod
    @router.post('/subject')
    async def subject_table(
            current_user: Annotated[User, Depends(user_manager.get_current_verified_user)],
            subject_name: str = Form()
    ):
        await subject_manager.create_object(
            {
                'subject_name': subject_name,
                'user_id': current_user.id,
                'id': str(uuid.uuid4())
            }
        )
        response = RedirectResponse('/tables/subject')
        response.status_code = 302
        return response

    @staticmethod
    @router.get('/subject-delete/{subject_id}')
    async def subject_table(
            subject_id: str,
            current_user: Annotated[User, Depends(user_manager.get_current_verified_user)],
    ):
        current_subject = await subject_manager.get_object_by_id(subject_id)
        if current_subject.user_id == current_user.id:
            await subject_manager.delete_object_by_id(subject_id)
            response = RedirectResponse('/tables/subject')
            response.status_code = 302
            return response
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail='You do not have permission to delete this subject'
        )


class ClassroomTableView:
    @staticmethod
    @router.get('/classroom')
    async def classroom_table(
            request: Request,
            current_user: Annotated[User, Depends(user_manager.get_current_verified_user)]
    ):
        subjects = await subject_manager.get_all_objects_by_user_id(current_user.id)
        classrooms = await classroom_manager.get_all_objects_by_user_id(current_user.id)
        subjects_classrooms = await subject_classroom_manager.get_all_associations_by_user_id(current_user.id)
        for subject, classroom in subjects_classrooms.items():
            print(subject.subject_name, classroom.type)
        return settings.templates.TemplateResponse(
            'classroom_table.html',
            {
                'request': request,
                'subjects': subjects,
                'classrooms': classrooms,
                'subjects_classrooms': subjects_classrooms
            }
        )

    @staticmethod
    @router.post('/classroom')
    async def classroom_table(
            current_user: Annotated[User, Depends(user_manager.get_current_verified_user)],
            name: str = Form(),
            _type: str = Form(),
            subject: str = Form(),
    ):
        classroom_id = str(uuid.uuid4())
        await classroom_manager.create_object(
            {
                'name': name,
                'type': _type,
                'user_id': current_user.id,
                'id': classroom_id
            }
        )
        subjects = await subject_manager.get_all_objects_by_user_id(current_user.id)
        for _subject in subjects:
            if _subject.subject_name == subject:
                await subject_classroom_manager.create_association(
                    subject_id=_subject.id,
                    classroom_id=classroom_id,
                    user_id=current_user.id,
                    _id=str(uuid.uuid4())
                )
                response = RedirectResponse('/tables/classroom')
                response.status_code = 302
                return response
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Relation not found'
        )

    @staticmethod
    @router.get('/classroom-delete/{subject_id}/{classroom_id}')
    async def delete_classroom(
            subject_id: str,
            classroom_id: str,
            current_user: Annotated[User, Depends(user_manager.get_current_verified_user)],
    ):
        current_classroom = await classroom_manager.get_object_by_id(classroom_id)
        if current_classroom.user_id == current_user.id:
            await classroom_manager.delete_object_by_id(current_classroom.id)
            await subject_classroom_manager.delete_association(
                classroom_id=classroom_id,
                subject_id=subject_id
            )
            response = RedirectResponse('/tables/classroom')
            response.status_code = 302
            return response
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail='You do not have permission to delete this classroom'
        )
