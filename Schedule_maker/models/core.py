from typing import List
from uuid import uuid4

from sqlalchemy import ForeignKey
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, declared_attr, relationship


class Base(declarative_base()):
    __abstract__ = True

    id: Mapped[str] = mapped_column(primary_key=True, default=str(uuid4()))

    @classmethod
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


class User(Base):
    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str] = mapped_column(nullable=True)
    is_google_user: Mapped[bool] = mapped_column(default=False)
    is_verified: Mapped[bool] = mapped_column(default=False)

    teachers: Mapped[List['Teacher']] = relationship(backref='user')
    subjects: Mapped[List['Subject']] = relationship(backref='user')
    groups: Mapped[List['Group']] = relationship(backref='user')
    classrooms: Mapped[List['Classroom']] = relationship(backref='user')
    curriculums: Mapped[List['Curriculum']] = relationship(backref='user')
    schedules: Mapped[List['Schedule']] = relationship(backref='user')

    def __init__(self, email, hashed_password):
        self.email = email
        self.hashed_password = hashed_password


class Subject(Base):
    subject_name: Mapped[str]

    user_id: Mapped[str] = mapped_column(
        ForeignKey(
            column='user.id',
            ondelete='CASCADE'
        )
    )


class Teacher(Base):
    full_name: Mapped[str]

    user_id: Mapped[str] = mapped_column(
        ForeignKey(
            column='user.id',
            ondelete='CASCADE',
        )
    )

    def __init__(self, full_name, user_id, _id):
        self.full_name = full_name
        self.user_id = user_id
        self.id = _id


class Group(Base):
    group_name: Mapped[str] = mapped_column(unique=True)

    user_id: Mapped[str] = mapped_column(
        ForeignKey(
            column='user.id',
            ondelete='CASCADE'
        )
    )

    curriculum_id: Mapped[str] = mapped_column(
        ForeignKey(
            column='curriculum.id',
            ondelete='CASCADE'
        )
    )


class Classroom(Base):
    name: Mapped[str]
    type: Mapped[str]

    user_id: Mapped[str] = mapped_column(
        ForeignKey(
            column='user.id',
            ondelete='CASCADE'
        )
    )


class Curriculum(Base):
    name: Mapped[str]
    stream: Mapped[str]

    amount_lectures: Mapped[int]
    amount_practices: Mapped[int]
    amount_labs: Mapped[int]

    user_id: Mapped[str] = mapped_column(
        ForeignKey(
            column='user.id',
            ondelete='CASCADE'
        )
    )

    groups: Mapped[List['Group']] = relationship(backref='curriculum')


class ClassroomSubject(Base):
    user_id: Mapped[str] = mapped_column(
        ForeignKey(
            column='user.id',
            ondelete='CASCADE'
        )
    )

    subject_id: Mapped[str] = mapped_column(
        ForeignKey(
            column='subject.id',
            ondelete='CASCADE'
        )
    )

    classroom_id: Mapped[str] = mapped_column(
        ForeignKey(
            column='classroom.id',
            ondelete='CASCADE'
        )
    )


class SubjectTeacher(Base):
    user_id: Mapped[str] = mapped_column(
        ForeignKey(
            column='user.id',
            ondelete='CASCADE'
        )
    )

    subject_id: Mapped[str] = mapped_column(
        ForeignKey(
            column='subject.id',
            ondelete='CASCADE'
        )
    )

    teacher_id: Mapped[str] = mapped_column(
        ForeignKey(
            column='teacher.id',
            ondelete='CASCADE'
        )
    )


class CurriculumSubject(Base):
    user_id: Mapped[str] = mapped_column(
        ForeignKey(
            column='user.id',
            ondelete='CASCADE'
        )
    )

    subject_id: Mapped[str] = mapped_column(
        ForeignKey(
            column='subject.id',
            ondelete='CASCADE'
        )
    )

    curriculum_id: Mapped[str] = mapped_column(
        ForeignKey(
            column='curriculum.id',
            ondelete='CASCADE'
        )
    )


class Schedule(Base):
    user_id: Mapped[str] = mapped_column(
        ForeignKey(
            column='user.id',
            ondelete='CASCADE'
        )
    )
