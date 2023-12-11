"""Generating schedule"""
import random
import asyncio

import controller.xlsx.createXLSX as xlsx
from controller.containers import Course
from serializer.Serializer import serializer


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

    def __init__(self, subjects, groups, plans, classrooms):

        # {name of subject: amount of teachers}
        self.subjects = subjects
        print(self.subjects)

        # {group number: curriculum number}
        self.groups = groups
        print(groups)
        # {subject name: Course object}
        self.plans = plans
        for plan in plans:
            print(plan, ":")
            for subject in plans[plan]:
                print(subject, ":", plans[plan][subject].lectures, plans[plan][subject].practicals,
                        plans[plan][subject].labs, plans[plan][subject].stream)

        self.classrooms = classrooms
        for classroom in classrooms:
            print(classroom.name, classroom.type, classroom.subjects)

        self.lessons_per_week = xlsx.days_of_study * xlsx.lessons_per_day

    def generate_all_lessons(self):
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
                teacher = random.choice(self.subjects[lesson])
                found = False
                for amount in range(6):
                    if {lesson: [self.plans[plan][lesson].stream, teacher, amount]} in all_lessons:
                        found = True
                        break
                if not found:
                    for i in range(self.plans[plan][lesson].lectures):
                        amount = 0
                        for stream in self.plans:
                            try:
                                if self.plans[stream][lesson].stream == self.plans[plan][lesson].stream:
                                    for group in self.groups:
                                        if self.groups[group] == stream:
                                            amount += 1
                            except KeyError:
                                ...
                        # print({lesson: [self.plans[plan][lesson].stream, teacher, amount]})
                        all_lessons.append({lesson: [self.plans[plan][lesson].stream, teacher, amount]})

        for group in self.groups:
            lessons = self.plans.get(self.groups.get(group))
            for lesson in lessons:
                teacher = random.choice(self.subjects[lesson])
                for i in range(lessons.get(lesson).practicals):
                    all_lessons.append({lesson: [group, teacher]})
                for i in range(lessons.get(lesson).labs):
                    all_lessons.append({lesson: [group + 'lab', teacher]})

        print(all_lessons)
        return all_lessons

    def generate_schedule(self, all_lessons):
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
        for subject in self.subjects:
            for teacher in self.subjects[subject]:
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
                                    classroom.type == 'Лекция'):
                                amount = 0
                                for group in self.groups.keys():
                                    try:
                                        # print(i, group)
                                        if (self.plans[self.groups[group]][list(lesson.keys())[0]].stream
                                                == self.plans[plan][list(lesson.keys())[0]].stream
                                                and free_time[group][i] == [0, 0]):
                                            amount += 1

                                    except KeyError:
                                        ...
                                if amount == list(lesson.values())[0][2]:
                                    for group in self.groups.keys():
                                        try:
                                            # print(i, group)
                                            if (self.plans[self.groups[group]][list(lesson.keys())[0]].stream
                                                    == self.plans[plan][list(lesson.keys())[0]].stream
                                                    and free_time[group][i] == [0, 0]):
                                                amount += 1
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

                                                # print(schedule)

                                        except KeyError:
                                            ...
                                    lesson_id += 1
                                    all_lessons.remove(lesson)
                                    free_classrooms[i].remove(classroom)

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

                        if flag and free_time[group][i][j] == 0:
                            for classroom in free_classrooms[i]:
                                if (list(lesson.keys())[0] in classroom.subjects and
                                        classroom.type == 'Лабораторная'):

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

                    if flag and free_time[group][i] == [0, 0]:
                        for classroom in free_classrooms[i]:
                            if (list(lesson.keys())[0] in classroom.subjects and
                                    classroom.type == 'Практика'):

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
        lessons = self.generate_all_lessons()

        schedule, free_time, teachers = self.generate_schedule(lessons)
        print(schedule)

        xlsx.schedule_to_xlsx(schedule, free_time, teachers)


if __name__ == '__main__':
    generator = ScheduleGenerator(
        asyncio.run(serializer.get_subject()),
        asyncio.run(serializer.get_group()),
        asyncio.run(serializer.get_curriculum()),
        asyncio.run(serializer.get_classroom())
    )
    generator.main()
