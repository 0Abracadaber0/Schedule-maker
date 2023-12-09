"""Generating schedule"""
import enum
import random

from itertools import count
from faker import Faker

import controller.xlsx.createXLSX as xlsx


class Const(enum.Enum):
    Lecture = 1
    Practice = 2
    Lab = 3


def is_end_lab(s):
    """Checks the string for 'lab' at the end

    Args:
        s: string for check

    Returns: True/False

    """
    if len(s) < 3:
        return False
    return s[-3:] == 'lab'


class ScheduleGenerator:
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

    def __init__(self):
        # faker for generate teacher's names
        self.faker = Faker()
        self.names = (self.faker.name() for _ in count())

        # {name of subject: amount of teachers}
        self.subjects = {
            'Алгоритмы и структуры данных': 2,
            'math': 3,
            'art': 2,
            'science': 2,
            'history': 2,
            'music': 2,
            'geography': 2,
            'P.E.': 2,
            'I.T.': 2,
            'biology': 2
        }

        # {group number: curriculum number}
        self.groups = {
            '10701122': 1,
            '10701222': 1,
            '10701322': 1,
            '10702122': 2,
            '10702222': 2,
            '10702322': 3,
            '10702422': 3
        }

        # {subject name: Course object}
        self.plans = {
            1: {
                'Алгоритмы и структуры данных': self.Course(1, 0, 2, '1'),
                'math': self.Course(1, 2, 0, '1'),
                'science': self.Course(1, 1, 1, '1'),
                'geography': self.Course(1, 1, 0, '1'),
                'I.T.': self.Course(1, 0, 1, '1'),
                'biology': self.Course(1, 1, 0, '1')
            },
            2: {
                'Алгоритмы и структуры данных': self.Course(1, 0, 1, '2'),
                'math': self.Course(1, 2, 0, '2'),
                'art': self.Course(1, 1, 0, '2'),
                'history': self.Course(1, 1, 0, '2'),
                'music': self.Course(1, 0, 1, '2'),
                'P.E.': self.Course(2, 0, 0, '2'),
                'biology': self.Course(1, 1, 0, '2')
            },
            3: {
                'Алгоритмы и структуры данных': self.Course(1, 0, 1, '3'),
                'math': self.Course(1, 2, 0, '3'),
                'I.T.': self.Course(1, 0, 1, '3'),
                'music': self.Course(1, 1, 0, '3'),
                'P.E.': self.Course(2, 0, 0, '2')
            }
        }

        self.classrooms = []

        classroom = self.Classroom('306', Const.Lecture, list(self.subjects.keys()))
        self.classrooms.append(classroom)

        classroom = self.Classroom('507', Const.Lecture, list(self.subjects.keys()))
        self.classrooms.append(classroom)

        classroom = self.Classroom('107', Const.Lecture, list(self.subjects.keys()))
        self.classrooms.append(classroom)

        classroom = self.Classroom('325', Const.Practice, list(self.subjects.keys()))
        self.classrooms.append(classroom)

        classroom = self.Classroom('326', Const.Practice, list(self.subjects.keys()))
        self.classrooms.append(classroom)

        classroom = self.Classroom('327', Const.Practice, list(self.subjects.keys()))
        self.classrooms.append(classroom)

        classroom = self.Classroom('116', Const.Practice, list(self.subjects.keys()))
        self.classrooms.append(classroom)

        classroom = self.Classroom('105', Const.Lab, list(self.subjects.keys()))
        self.classrooms.append(classroom)

        classroom = self.Classroom('313', Const.Lab, list(self.subjects.keys()))
        self.classrooms.append(classroom)

        classroom = self.Classroom('329', Const.Lab, list(self.subjects.keys()))
        self.classrooms.append(classroom)

        classroom = self.Classroom('407', Const.Lab, list(self.subjects.keys()))
        self.classrooms.append(classroom)

        classroom = self.Classroom('420', Const.Lab, list(self.subjects.keys()))
        self.classrooms.append(classroom)

        self.lessons_per_week = xlsx.days_of_study * xlsx.lessons_per_day

    def generate_teacher(self):
        """Generate teacher's names
        Returns:
            A fake teacher's name
        """
        return next(name for name in self.names)

    def link_all_subjects(self):
        """
        Returns:
            A dict mapped subject's name to the list of teacher's names.
            For example:

            {
                'math': ['Laura Hill', 'Adam Smith'],
                'art': ['Heather Galloway'],
                'biology': ['Martha Allen', 'Lisa Cook']
            }
        """
        teachers = {}
        for subject in self.subjects:
            teachers.update({subject: [self.generate_teacher() for _ in range(self.subjects.get(subject))]})

        return teachers

    def generate_all_lessons(self, teachers):
        """Create a list of unique lessons

        Args:
            teachers: A dict mapped subject's name to the list of teacher's names.

        Returns:
            A list of unique lessons.
            For example:

            [
                {'P.E.': ['10702222', 'Deanna Newton']},
                {'biology': ['10702222', 'Kara Romero']},
                {'math': ['10702322', 'Rachel Young']},
                {'math': ['10702322', 'Rachel Young']},
                {'art': ['10702322', 'Jason Mullins']}
            ]
        """
        all_lessons = []
        for plan in self.plans:
            for lesson in self.plans[plan]:
                teacher = random.choice(teachers[lesson])
                if {lesson: [self.plans[plan][lesson].stream, teacher]} not in all_lessons:
                    for i in range(self.plans[plan][lesson].lectures):
                        all_lessons.append({lesson: [self.plans[plan][lesson].stream, teacher]})

        for group in self.groups:
            lessons = self.plans.get(self.groups.get(group))
            for lesson in lessons:
                teacher = random.choice(teachers[lesson])
                for i in range(lessons.get(lesson).practicals):
                    all_lessons.append({lesson: [group, teacher]})
                for i in range(lessons.get(lesson).labs):
                    all_lessons.append({lesson: [group + 'lab', teacher]})

        return all_lessons

    def generate_schedule(self, all_lessons, subjects_teachers):
        """Distributes lessons in such a way that groups and teachers do not overlap at the same time.

        Args:
            subjects_teachers: A dict mapped subjects and arrays of teachers.
            all_lessons: A list of unique lessons.

        Returns: A dict mapped group's number and array of subject's name and teacher's name.
                 For example:

                 {
                    '10701122': [['math', 'James Walters'], ['math', 'James Walters'], [0]],
                    '10701222': [['science', 'Charles Farmer'], [0], [0]]
                 }

                 A dict mapped group's number and array of id of every lesson.
                 For example:

                 {
                    '10701122': [[1, 1], [3, 3], [4, 0], [0, 0] [6, 6]],
                    '10701222': [[1, 1], [2, 2], [0, 0], [5, 0], [0, 0]]
                 }

                 A dict mapped teacher's name and lesson.
                 For example:

                 {
                    'Jessica Ward': [['math', '10701122 10701222'], [0, '']],
                    'Linda Short': [['P.E.', '10702122'], ['P.E.', '10702222']]
                 }

        """
        # 0 - time is free, else - not
        free_time = {key: [[0, 0] for _ in range(self.lessons_per_week)] for key in self.groups.keys()}

        free_classrooms = [self.classrooms.copy() for _ in range(self.lessons_per_week)]

        lesson_id = 1

        teachers = {}
        for subject in subjects_teachers:
            for teacher in subjects_teachers[subject]:
                teachers[teacher] = [[0, '', ''] for _ in range(self.lessons_per_week)]

        schedule = {key: [[[0, 0, 0], [0, 0, 0]] for _ in range(self.lessons_per_week)] for key in self.groups.keys()}

        for i in range(self.lessons_per_week):
            for plan in self.plans:
                for lesson in all_lessons:
                    try:
                        if lesson[list(lesson.keys())[0]][0] != self.plans[plan][list(lesson.keys())[0]].stream:
                            continue
                    except KeyError:
                        continue

                    flag = True
                    for key in schedule.keys():
                        if schedule[key][i][1][1] == lesson[list(lesson.keys())[0]][1]:
                            flag = False

                            break

                    if flag:
                        for classroom in free_classrooms[i]:
                            if (list(lesson.keys())[0] in classroom.subjects and
                                    classroom.type == Const.Lecture):
                                for group in self.groups.keys():
                                    try:

                                        if (self.plans[self.groups[group]][list(lesson.keys())[0]].stream
                                                == self.plans[plan][list(lesson.keys())[0]].stream):

                                            free_time[group][i] = [lesson_id, lesson_id]

                                            teachers[list(lesson.values())[0][1]][i][0] = list(lesson.keys())[0]
                                            teachers[list(lesson.values())[0][1]][i][1] += ' ' + group
                                            teachers[list(lesson.values())[0][1]][i][2] = classroom.name

                                            schedule[group][i][0][0] = list(lesson.keys())[0]
                                            schedule[group][i][0][1] = list(lesson.values())[0][1]
                                            schedule[group][i][0][2] = classroom.name

                                            schedule[group][i][1][0] = list(lesson.keys())[0]
                                            schedule[group][i][1][1] = list(lesson.values())[0][1]
                                            schedule[group][i][1][2] = classroom.name

                                            # print('accepted:', group, schedule[group][i])
                                    except KeyError:
                                        pass
                                lesson_id += 1
                                all_lessons.remove(lesson)
                                free_classrooms[i].remove(classroom)

                                break

        for i in range(self.lessons_per_week):
            for group in schedule:
                for j in range(2):
                    if free_time[group][i][j] != 0:
                        continue
                    for lesson in all_lessons:
                        if not is_end_lab(lesson[list(lesson.keys())[0]][0]):
                            continue
                        if lesson[list(lesson.keys())[0]][0][:-3] != group:
                            continue

                        flag = True
                        for key in schedule.keys():
                            if (schedule[key][i][0][1] == lesson[list(lesson.keys())[0]][1]
                                    or schedule[key][i][1][1] == lesson[list(lesson.keys())[0]][1]):
                                flag = False

                                break

                        if flag:
                            for classroom in free_classrooms[i]:
                                if (list(lesson.keys())[0] in classroom.subjects and
                                        classroom.type == Const.Lab):

                                    free_time[group][i][j] = lesson_id
                                    lesson_id += 1

                                    teachers[list(lesson.values())[0][1]][i][0] = list(lesson.keys())[0]
                                    teachers[list(lesson.values())[0][1]][i][1] += ' ' + group
                                    teachers[list(lesson.values())[0][1]][i][2] = classroom.name

                                    schedule[group][i][j][0] = list(lesson.keys())[0]
                                    schedule[group][i][j][1] = list(lesson.values())[0][1]
                                    schedule[group][i][j][2] = classroom.name

                                    all_lessons.remove(lesson)
                                    free_classrooms[i].remove(classroom)

                                    break

        for i in range(self.lessons_per_week):
            for group in schedule:
                if free_time[group][i] != [0, 0]:
                    continue
                for lesson in all_lessons:

                    if lesson[list(lesson.keys())[0]][0] != group:
                        continue

                    flag = True
                    for key in schedule.keys():
                        if (schedule[key][i][0][1] == lesson[list(lesson.keys())[0]][1]
                                or schedule[key][i][1][1] == lesson[list(lesson.keys())[0]][1]):
                            flag = False

                            break

                    if flag:
                        for classroom in free_classrooms[i]:
                            if (list(lesson.keys())[0] in classroom.subjects and
                                    classroom.type == Const.Practice):
                                free_time[group][i] = [lesson_id, lesson_id]
                                lesson_id += 1

                                teachers[list(lesson.values())[0][1]][i][0] = list(lesson.keys())[0]
                                teachers[list(lesson.values())[0][1]][i][1] += ' ' + group
                                teachers[list(lesson.values())[0][1]][i][2] = classroom.name

                                schedule[group][i][0][0] = list(lesson.keys())[0]
                                schedule[group][i][0][1] = list(lesson.values())[0][1]
                                schedule[group][i][0][2] = classroom.name

                                schedule[group][i][1][0] = list(lesson.keys())[0]
                                schedule[group][i][1][1] = list(lesson.values())[0][1]
                                schedule[group][i][1][2] = classroom.name

                                # print('accepted:', group, schedule[group][i], i)

                                all_lessons.remove(lesson)
                                free_classrooms[i].remove(classroom)

                                break

        return schedule, free_time, teachers

    def main(self):
        teachers = self.link_all_subjects()

        lessons = self.generate_all_lessons(teachers)

        schedule, free_time, teachers = self.generate_schedule(lessons, teachers)
        print(schedule)

        xlsx.schedule_to_xlsx(schedule, free_time, teachers)


if __name__ == '__main__':
    generator = ScheduleGenerator()
    generator.main()
