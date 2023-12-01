from datetime import (
    datetime
)
from typing import (
    List
)

from sqlalchemy import (
    func,
    ForeignKey,
    Integer
)
from sqlalchemy.orm import (
    Mapped,
    relationship,
    mapped_column
)
from sqlalchemy.ext.declarative import (
    declared_attr
)
from sqlalchemy.orm import (
    declarative_base
)
from fastapi_users.db import (
    SQLAlchemyBaseUserTable
)


class Base(declarative_base()):
    __abstract__ = True

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    @classmethod
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


class User(SQLAlchemyBaseUserTable[int], Base):
    username: Mapped[str] = mapped_column(unique=True)
    email: str
    hashed_password: str
    is_active: bool
    is_superuser: bool
    is_verified: bool

    teachers: Mapped[List['Teacher']] = relationship(backref='user')
    subjects: Mapped[List['Subject']] = relationship(backref='user')
    groups: Mapped[List['Group']] = relationship(backref='user')
    token: Mapped['Token'] = relationship(backref='user')

    def __init__(self, username, email, hashed_password):
        self.email = email
        self.username = username
        self.hashed_password = hashed_password


class Token(Base):
    access_token: Mapped[str]
    user_id = mapped_column(
        ForeignKey(
            column='user.id',
            ondelete='CASCADE'
        )
    )

    def __init__(self, user_id, token):
        self.user_id = user_id
        self.access_token = token


class Teacher(Base):
    full_name: Mapped[str]

    user_id: Mapped[int] = mapped_column(
        ForeignKey(
            column='user.id',
            ondelete='CASCADE'
        )
    )


class Subject(Base):
    subject_name: Mapped[str]

    user_id: Mapped[int] = mapped_column(
        ForeignKey(
            column='user.id',
            ondelete='CASCADE'
        )
    )


class Group(Base):
    group_name: Mapped[str]

    user_id: Mapped[int] = mapped_column(
        ForeignKey(
            column='user.id',
            ondelete='CASCADE'
        )
    )
