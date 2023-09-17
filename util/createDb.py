from sqlalchemy_utils import database_exists
from sqlalchemy import create_engine, URL, ForeignKey, Column, String, Integer, PrimaryKeyConstraint
from sqlalchemy.orm import declarative_base
from sqlalchemy.exc import ArgumentError


Base = declarative_base()


class Teacher(Base):
    __tablename__ = 'teacher'

    teacher_id = Column('teacher_id', Integer, primary_key=True)
    teacher_name_surname = Column('teacher_name_surname', String)
    hour_load = Column('hour_load', Integer)


class Subject(Base):
    __tablename__ = 'subject'

    subject_id = Column('subject_id', Integer, primary_key=True)
    subject_name = Column('subject_name', String)
    subject_lecture_count = Column('subject_lecture_count', Integer)
    subject_practice_count = Column('subject_practice_count', Integer)
    subject_lab_count = Column('subject_lab_count', Integer)


class Specialization(Base):
    __tablename__ = 'specialization'

    specialization_id = Column('specialization_id', Integer, primary_key=True)
    specialization_name = Column('specialization_name', String)


class Auditorium(Base):
    __tablename__ = 'auditorium'

    auditorium_id = Column('auditorium_id', Integer, primary_key=True)
    auditorium_type = Column('auditorium_type', String)
    auditorium_capacity = Column('auditorium_capacity ', Integer)


class Group(Base):
    __tablename__ = 'group'

    group_id = Column('group_id', Integer, primary_key=True)
    specialization_id = Column(Integer, ForeignKey('specialization.specialization_id'))


class Student(Base):
    __tablename__ = 'student'

    student_id = Column('student_id', Integer, primary_key=True)
    student_name = Column('student_name', String)
    group_id = Column(Integer, ForeignKey('group.group_id'))


class TeachersSubjects(Base):
    __tablename__ = 'teachers_subjects'
    __table_args__ = (
        PrimaryKeyConstraint('teacher_id', 'subject_id'),
    )

    teacher_id = Column(Integer, ForeignKey('teacher.teacher_id'))
    subject_id = Column(Integer, ForeignKey('subject.subject_id'))


class SubjectsSpecializations:
    __tablename__ = 'subjects_specializations'
    __table_args__ = (
        PrimaryKeyConstraint('subject_id', 'specialization_id'),
    )

    subject_id = Column(Integer, ForeignKey('subject.subject_id'))
    specialization_id = Column(Integer, ForeignKey('specialization.specialization_id'))


class SubjectsAuditoriums:
    __tablename__ = 'subjects_auditoriums'
    __table_args__ = (
        PrimaryKeyConstraint('subject_id', 'auditorium_id'),
    )

    subject_id = Column(Integer, ForeignKey('subject.subject_id'))
    auditorium_id = Column(Integer, ForeignKey('auditorium.auditorium_id'))


def get_url(_user, _password, _host, _port, _db):
    try:
        url_obj = URL(
            'postgresql',
            username=_user,
            password=_password,
            host=_host,
            port=_port,
            database=_db,
            query={}
        )
        if not database_exists(url_obj):
            return None
        else:
            return url_obj
    except ValueError:
        raise ValueError


if __name__ == '__main__':
    try:
        engine = create_engine(get_url(
                 input('user: '),
                 input('password: '),
                 input('host: '),
                 input('port: '),
                 input('dbname: ')
                )
        )
        Base.metadata.create_all(bind=engine)
        print('Success: settings have been imported!')
    except (ArgumentError, ValueError):
        print('Error: connection failed!')
