"""Generating schedule"""
import random

from itertools import count
from faker import Faker

import model.xlsx.createXLSX as xlsx


class ScheduleGenerator:
    def __init__(self):
        # faker for generate teacher's names
        self.faker = Faker()
        self.names = (self.faker.name() for _ in count())

        # {name of subject: amount of teachers}
        self.subjects = {
            'Алгоритмы и структуры данных': 1,
            'math': 2,
            'art': 1,
            'science': 1,
            'history': 1,
            'music': 1,
            'geography': 1,
            'P.E.': 1,
            'I.T.': 1,
            'biology': 1
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

        # {subject name: [amount of lectures, amount of practical lessons, stream's number]}
        self.plans = {
            1: {
                'Алгоритмы и структуры данных': [1, 2, '1'],
                'math': [1, 2, '1'],
                'science': [1, 3, '1'],
                'geography': [1, 1, '1'],
                'I.T.': [1, 1, '1'],
                'biology': [1, 1, '1']
            },
            2: {
                'Алгоритмы и структуры данных': [1, 1, '2'],
                'math': [1, 2, '2'],
                'art': [1, 1, '2'],
                'history': [1, 1, '2'],
                'music': [1, 1, '2'],
                'P.E.': [2, 0, '2'],
                'biology': [1, 1, '2']
            },
            3: {
                'Алгоритмы и структуры данных': [1, 1, '3'],
                'math': [1, 2, '3'],
                'I.T.': [1, 1, '3'],
                'music': [1, 1, '3'],
                'P.E.': [2, 0, '2']
            }
        }

        self.lessons_per_week = xlsx.days_of_study * xlsx.lessons_per_day

    def generate_teacher(self):
        """Generate teacher's names
        Returns:
            A fake teacher's name
        """
        return next(name for name in self.names
                    )

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

                for i in range(self.plans[plan][lesson][0]):
                    all_lessons.append({lesson: [self.plans[plan][lesson][2], teacher]})

        for group in self.groups:
            lessons = self.plans.get(self.groups.get(group))
            for lesson in lessons:
                teacher = random.choice(teachers[lesson])
                for i in range(lessons.get(lesson)[1]):
                    all_lessons.append({lesson: [group, teacher]})

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
                    '10701122': [1, 3, 4, 0, 6],
                    '10701222': [1, 2, 0, 5, 0]
                 }

                 A dict mapped teacher's name and lesson.
                 For example:

                 {
                    'Jessica Ward': [['math', '10701122 10701222'], [0, '']],
                    'Linda Short': [['P.E.', '10702122'], ['P.E.', '10702222']]
                 }

        """
        # 0 - time is free, else - not
        free_time = {key: [0] * self.lessons_per_week for key in self.groups.keys()}
        lesson_id = 1

        teachers = {}
        for subject in subjects_teachers:
            for teacher in subjects_teachers[subject]:
                teachers[teacher] = [[0, ''] for _ in range(self.lessons_per_week)]

        schedule = {key: [[0, 0] for _ in range(self.lessons_per_week)] for key in self.groups.keys()}

        for i in range(self.lessons_per_week):
            for plan in self.plans:
                for lesson in all_lessons:
                    try:
                        if lesson[list(lesson.keys())[0]][0] != self.plans[plan][list(lesson.keys())[0]][2]:
                            continue
                    except KeyError:
                        continue

                    flag = True
                    for key in schedule.keys():
                        if schedule[key][i][1] == lesson[list(lesson.keys())[0]][1]:
                            flag = False

                            break

                    if flag:
                        for group in self.groups.keys():
                            try:

                                if (self.plans[self.groups[group]][list(lesson.keys())[0]][2]
                                        == self.plans[plan][list(lesson.keys())[0]][2]):
                                    free_time[group][i] = lesson_id

                                    teachers[list(lesson.values())[0][1]][i][0] = list(lesson.keys())[0]
                                    teachers[list(lesson.values())[0][1]][i][1] += ' ' + group

                                    schedule[group][i][0] = list(lesson.keys())[0]
                                    schedule[group][i][1] = list(lesson.values())[0][1]

                                    print('accepted:', group, schedule[group][i])
                            except KeyError:
                                pass
                        lesson_id += 1
                        all_lessons.remove(lesson)

                        break

                    else:
                        print('nope:', list(lesson.keys())[0], list(lesson.values())[0][1])

        for i in range(self.lessons_per_week):
            for group in schedule:
                if free_time[group][i] != 0:
                    continue

                for lesson in all_lessons:

                    if lesson[list(lesson.keys())[0]][0] != group:
                        continue

                    flag = True
                    for key in schedule.keys():
                        if schedule[key][i][1] == lesson[list(lesson.keys())[0]][1]:
                            flag = False

                            break

                    if flag:
                        free_time[group][i] = lesson_id
                        lesson_id += 1

                        teachers[list(lesson.values())[0][1]][i][0] = list(lesson.keys())[0]
                        teachers[list(lesson.values())[0][1]][i][1] += ' ' + group

                        schedule[group][i][0] = list(lesson.keys())[0]
                        schedule[group][i][1] = list(lesson.values())[0][1]

                        print('accepted:', group, schedule[group][i])

                        all_lessons.remove(lesson)

                        break

                    else:
                        print('nope:', list(lesson.keys())[0], list(lesson.values())[0][1])

        return schedule, free_time, teachers

    def main(self):
        teachers = self.link_all_subjects()

        lessons = self.generate_all_lessons(teachers)

        schedule, free_time, teachers = self.generate_schedule(lessons, teachers)

        xlsx.schedule_to_xlsx(schedule, free_time, teachers)


if __name__ == '__main__':
    generator = ScheduleGenerator()
    generator.main()
