import enum


class Course:
    """
    Contains information about a course.
    """

    def __init__(self, lectures, practicals, labs, stream):
        self.lectures = lectures
        self.practicals = practicals
        self.labs = labs
        self.stream = stream


class Classroom:
    """
    A classroom
    """

    def __init__(self, name, type_of_classroom, subjects):
        self.name = name
        self.type = type_of_classroom
        self.subjects = subjects


class Const(enum.Enum):
    Lecture = 1
    Practice = 2
    Lab = 3
