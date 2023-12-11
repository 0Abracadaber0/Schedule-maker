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
from Schedule_maker.cruds.AssociationTableManager import (
    subject_classroom_manager, subject_teacher_manager, subject_curriculum_manager
)
from Schedule_maker.cruds.TableObjectManager import (
    teacher_manager, subject_manager, classroom_manager, curriculum_manager, group_manager
)


router = APIRouter()


class SubjectTeacherTableView:
    @staticmethod
    @router.get('/subject')
    async def subject_table(
            request: Request,
            current_user: Annotated[User, Depends(user_manager.get_current_verified_user)]
    ):
        subjects_teachers = await subject_teacher_manager.get_all_associations_by_user_id(current_user.id)
        return settings.templates.TemplateResponse('subject_table.html', {
            'request': request,
            'subjects_teachers': subjects_teachers
        })

    @staticmethod
    @router.post('/subject')
    async def subject_table(
            current_user: Annotated[User, Depends(user_manager.get_current_verified_user)],
            subject_name: str = Form(),
            full_name: str = Form()
    ):
        current_teacher_id = str(uuid.uuid4())
        current_subject_id = str(uuid.uuid4())
        await subject_manager.create_object(
            {
                'subject_name': subject_name,
                'user_id': current_user.id,
                'id': current_subject_id
            }
        )
        await teacher_manager.create_object(
            {
                'full_name': full_name,
                'user_id': current_user.id,
                'id': current_teacher_id
            }
        )

        await subject_teacher_manager.create_association(
            teacher_id=current_teacher_id,
            subject_id=current_subject_id,
            user_id=current_user.id,
            _id=str(uuid.uuid4())
        )

        response = RedirectResponse('/tables/subject')
        response.status_code = 302
        return response

    @staticmethod
    @router.get('/subject-delete/{subject_id}/{teacher_id}')
    async def subject_table(
            subject_id: str,
            teacher_id: str,
            current_user: Annotated[User, Depends(user_manager.get_current_verified_user)],
    ):
        current_subject = await subject_manager.get_object_by_id(subject_id)
        if current_subject.user_id == current_user.id:
            await subject_teacher_manager.delete_association(
                teacher_id=teacher_id,
                subject_id=subject_id
            )
            await subject_manager.delete_object_by_id(subject_id)
            await teacher_manager.delete_object_by_id(teacher_id)
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
            type: str = Form(),
            subject: str = Form(),
    ):
        classroom_id = str(uuid.uuid4())
        await classroom_manager.create_object(
            {
                'name': name,
                'type': type,
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
            await subject_classroom_manager.delete_association(
                classroom_id=classroom_id,
                subject_id=subject_id
            )
            await classroom_manager.delete_object_by_id(current_classroom.id)
            response = RedirectResponse('/tables/classroom')
            response.status_code = 302
            return response
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail='You do not have permission to delete this classroom'
        )


class CurriculumTableView:
    @staticmethod
    @router.get('/curriculum')
    async def curriculum_table(
            request: Request,
            current_user: Annotated[User, Depends(user_manager.get_current_verified_user)]
    ):
        print(f'\n\n\n\n{current_user.id}\n\n\n\n')
        subjects_curriculums = await subject_curriculum_manager.get_all_associations_by_user_id(
            user_id=current_user.id
        )
        subjects = await subject_manager.get_all_objects_by_user_id(
            user_id=current_user.id
        )
        return settings.templates.TemplateResponse(
            'curriculum_table.html',
            {
                'request': request,
                'subjects_curriculums': subjects_curriculums,
                'subjects': subjects
            }
        )

    @staticmethod
    @router.post('/curriculum')
    async def curriculum_table(
            current_user: Annotated[User, Depends(user_manager.get_current_verified_user)],
            subject_name: str = Form(), lectures: str = Form(), practices: str = Form(),
            labs: str = Form(), stream: str = Form(), name: str = Form()
    ):
        current_curriculum_id = str(uuid.uuid4())
        try:
            await curriculum_manager.create_object(
                {
                    'name': name,
                    'stream': stream,
                    'amount_lectures': int(lectures),
                    'amount_practices': int(practices),
                    'amount_labs': int(labs),
                    'user_id': current_user.id,
                    'id': current_curriculum_id
                }
            )
            user_subjects = await subject_manager.get_all_objects_by_user_id(current_user.id)
            if user_subjects:
                for subject in user_subjects:
                    if subject.subject_name == subject_name:
                        await subject_curriculum_manager.create_association(
                            curriculum_id=current_curriculum_id,
                            subject_id=subject.id,
                            user_id=current_user.id,
                            _id=str(uuid.uuid4())
                        )
                        response = RedirectResponse('/tables/curriculum')
                        response.status_code = 302
                        return response
        except TypeError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Please provide a valid input'
            )

    @staticmethod
    @router.get('/curriculum-delete/{subject_id}/{curriculum_id}')
    async def delete_curriculum(
            current_user: Annotated[User, Depends(user_manager.get_current_verified_user)],
            subject_id: str,
            curriculum_id: str
    ):
        current_curriculum = await curriculum_manager.get_object_by_id(curriculum_id)
        if current_curriculum.user_id == current_user.id:
            await subject_curriculum_manager.delete_association(
                curriculum_id=curriculum_id,
                subject_id=subject_id
            )
            await curriculum_manager.delete_object_by_id(curriculum_id)
            response = RedirectResponse('/tables/curriculum')
            response.status_code = 302
            return response

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='You do not have permission to delete this curriculum'
        )


class GroupTableView:
    @staticmethod
    @router.get("/group")
    async def group_table(
            request: Request,
            current_user: Annotated[User, Depends(user_manager.get_current_verified_user)]
    ):
        groups = await group_manager.get_all_objects_by_user_id(current_user.id)
        curriculums = await curriculum_manager.get_all_objects_by_user_id(current_user.id)
        groups_curriculums = []
        for group in groups:
            groups_curriculums.append(
                [
                    group,
                    await curriculum_manager.get_object_by_id(group.curriculum_id)
                ]
            )
        return settings.templates.TemplateResponse(
            'group_table.html',
            {
                'request': request,
                'curriculums': curriculums,
                'groups_curriculums': groups_curriculums
            }
        )

    @staticmethod
    @router.post("/group")
    async def group_table(
            current_user: Annotated[User, Depends(user_manager.get_current_verified_user)],
            group_name: str = Form(), curriculum: str = Form()
    ):
        current_group_id = str(uuid.uuid4())
        curriculum = await curriculum_manager.get_object_by_name(curriculum)
        if curriculum:
            await group_manager.create_object(
                {
                    'group_name': group_name,
                    'curriculum_id': curriculum.id,
                    'user_id': current_user.id,
                    'id': current_group_id
                }
            )
            response = RedirectResponse('/tables/group')
            response.status_code = 302
            return response
        raise HTTPException(
            status_code=status.HTTP_404_FORBIDDEN,
            detail='Curriculum does not exist'
        )

    @staticmethod
    @router.get("/group-delete/{group_id}")
    async def group_delete(
            current_user: Annotated[User, Depends(user_manager.get_current_verified_user)],
            group_id: str
    ):
        current_group = await group_manager.get_object_by_id(
            group_id
        )
        if current_group.user_id == current_user.id:
            await group_manager.delete_object_by_id(
                group_id
            )
            response = RedirectResponse('/tables/group')
            response.status_code = 302
            return response
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail='You do not have permission to delete this group'
        )
