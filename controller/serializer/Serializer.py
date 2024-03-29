from sqlalchemy import select

from Schedule_maker.models.db import Database
from Schedule_maker.models.core import (Group, Curriculum, CurriculumSubject, Subject, Classroom, ClassroomSubject,
                                        SubjectTeacher, Teacher)

from controller.containers import Course
from controller.containers import Classroom as ContainerClassroom


class Serializer:
    def __init__(self,
                 _db: Database,
                 user_id: str
                 ):
        self.db = _db
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
        async with (self.db.engine.begin() as session):
            coroutine_curriculums = await session.execute(
                select(Curriculum).where(Curriculum.user_id == self.user_id)
            )
            curriculums = coroutine_curriculums.fetchall()

            plans = {}
            for curriculum in curriculums:
                plans[curriculum.name] = {}

            for plan in plans:
                subjects = []
                for curriculum in curriculums:
                    if curriculum.name != plan:
                        continue
                    print(plan, curriculum)

                    coroutine_subject_id = await session.execute(
                        select(CurriculumSubject).where(CurriculumSubject.curriculum_id == curriculum.id)
                    )
                    subject_id = coroutine_subject_id.fetchone().subject_id

                    coroutine_subject = await session.execute(
                        select(Subject).where(Subject.id == subject_id)
                    )
                    subject = coroutine_subject.fetchone()
                    subjects.append({subject.subject_name: Course(curriculum.amount_lectures, curriculum.amount_practices,
                                                            curriculum.amount_labs, str(curriculum.stream))})

                for subject in subjects:
                    plans[plan][list(subject.keys())[0]] = list(subject.values())[0]

            return plans

    async def get_classroom(self):
        async with self.db.engine.begin() as session:
            coroutine_classrooms = await session.execute(
                select(Classroom).where(Classroom.user_id == self.user_id)
            )
            taken_classrooms = coroutine_classrooms.fetchall()

            subjects = []
            for taken_classroom in taken_classrooms:
                coroutine_subject_id = await session.execute(
                    select(ClassroomSubject).where(ClassroomSubject.classroom_id == taken_classroom.id)
                )
                subject_id = coroutine_subject_id.fetchone().subject_id

                coroutine_subject = await session.execute(
                    select(Subject).where(Subject.id == subject_id)
                )
                subject = coroutine_subject.fetchone()
                subjects.append(subject.subject_name)

            classrooms = []
            names = []
            for index, taken_classroom in enumerate(taken_classrooms):
                if taken_classroom.name not in names:
                    names.append(taken_classroom.name)
                    classrooms.append(
                        ContainerClassroom(
                            taken_classroom.name,
                            taken_classroom.type,
                            [subjects[index]]
                        )
                    )
                else:
                    for classroom in classrooms:
                        if classroom.name == taken_classroom.name:
                            classroom.subjects.append(subjects[index])

            return classrooms

    async def get_subject(self):
        async with self.db.engine.begin() as session:
            coroutine_subject = await session.execute(
                select(Subject).where(Subject.user_id == self.user_id)
            )
            taken_subjects = coroutine_subject.fetchall()
            teachers = []
            for taken_subject in taken_subjects:
                print(taken_subject)
                coroutine_teacher_id = await session.execute(
                    select(SubjectTeacher).where(SubjectTeacher.subject_id == taken_subject.id)
                )
                teacher_id = coroutine_teacher_id.fetchone().teacher_id
                coroutine_teacher = await session.execute(
                    select(Teacher).where(Teacher.id == teacher_id)
                )
                teacher = coroutine_teacher.fetchone()
                teachers.append(teacher)

            subjects = {}
            for index, taken_subject in enumerate(taken_subjects):
                try:
                    subjects[taken_subject.subject_name].append(teachers[index].full_name)
                except KeyError:
                    subjects[taken_subject.subject_name] = [teachers[index].full_name]

            return subjects
