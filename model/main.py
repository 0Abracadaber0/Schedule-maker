"""Generating schedule"""
import random

from itertools import count
from faker import Faker

import model.xlsx.createXLSX as xlsx

# faker for generate teacher's names
faker = Faker()
names = (faker.name() for _ in count())

# {name of subject: amount of teachers}
subjects = {
    'Алгоритмы и структуры данных': 2,
    'math': 2,
    'art': 1,
    'science': 1,
    'history': 1,
    'music': 1,
    'geography': 1,
    'P.E.': 1,
    'I.T.': 1,
    'biology': 2
}

# {group number: curriculum number}
groups = {
    '10701122': 1,
    '10701222': 1,
    '10701322': 1,
    '10702122': 2,
    '10702222': 2,
    '10702322': 2,
    '10702422': 2
}

# {curriculum number: {subject name: [amount of lectures, amount of practical lessons]}}
plans = {
    1: {
        'Алгоритмы и структуры данных': [1, 2],
        'math': [2, 2],
        'science': [1, 3],
        'geography': [1, 1],
        'I.T.': [1, 1],
        'biology': [1, 1]
    },
    2: {
        'Алгоритмы и структуры данных': [1, 1],
        'math': [1, 2],
        'art': [0, 1],
        'history': [1, 1],
        'music': [0, 1],
        'P.E.': [0, 2],
        'biology': [1, 1]
    }
}

lessons_per_week = xlsx.days_of_study * xlsx.lessons_per_day


def generate_teacher():
    """Generate teacher's names
    Returns:
        A fake teacher's name
    """
    return next(name for name in names)


def link_all_subjects():
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
    for subject in subjects:
        teachers.update({subject: [generate_teacher() for _ in range(subjects.get(subject))]})

    return teachers


def generate_all_lessons(teachers):
    """Create a list of unique lessons

    Args:
        teachers: A dict mapped subject's name to the list of teacher's names.

    Returns:
        A list of unique lessons.
        For example:

        [
            {'P.E.': {'Deanna Newton', '10702222'}},
            {'biology': {'10702222', 'Kara Romero'}},
            {'math': {'10702322', 'Rachel Young'}},
            {'math': {'10702322', 'Rachel Young'}},
            {'art': {'10702322', 'Jason Mullins'}}
        ]
    """
    all_lessons = []
    for stream in plans.keys():
        for lesson in plans[stream]:
            teacher = random.choice(teachers[lesson])
            for i in range(len(plans[stream])):
                all_lessons.append({lesson: {stream, teacher}})

    for group in groups:
        lessons = plans.get(groups.get(group))
        for lesson in lessons:
            teacher = random.choice(teachers[lesson])
            for i in range(lessons.get(lesson)[1]):
                all_lessons.append({lesson: {group, teacher}})

    return all_lessons


def generate_schedule(all_lessons):
    """Distributes lessons in such a way that groups and teachers do not overlap at the same time.

    Args:
        all_lessons: A list of unique lessons.

    Returns:
        A two-dimensional array where a row is a time unit and a column is a group or stream.
        For example:

        [
            {'science': {1, 'Kelly Davidson'}},
            {'art': {2, 'John Flores'}},
            {0: {0}},
            {'math': {'10702422', 'Tracy Morse'}},
        ]
    """
    schedule = [[{0: {0, 0}}] * len(groups) for _ in range(lessons_per_week)]
    for row in schedule:
        for index, element in enumerate(row):
            f = True
            for lesson in all_lessons:
                f = True
                key = next(iter(lesson))

                for i in range(index):
                    i_key = next(iter(row[i]))
                    if not lesson[key].isdisjoint(row[i][i_key]):
                        f = False
                        break
                if f:
                    row[index] = lesson
                    all_lessons.remove(lesson)
                    break
            if f:
                continue

    return schedule


def schedule_by_groups(schedule):
    """Remake a two-dimensional array obtained from the function generate_schedule

    Args:
        schedule: A two-dimensional array where a row is a time unit and a column is a group or stream.

    Returns: A dict mapped group's number and array of subject's name and teacher's name.
             For example:

             {
                '10701122': [['math', 'James Walters'], ['math', 'James Walters'], [0]],
                '10701222': [['science', 'Charles Farmer'], [0], [0]]
             }

    """
    # 0 - time is free, 1 - time isn't free
    free_time = {key: [0] * lessons_per_week for key in groups.keys()}

    groups_lessons = groups
    for group in groups_lessons:
        groups_lessons[group] = []

    size = 0
    for row in schedule:
        size += 1
        for elem in row:
            for key, value in elem.items():
                for group in groups_lessons:
                    if not value.isdisjoint({group}):
                        for set_elem in value:
                            if group != set_elem and free_time[group][size-1] == 0:
                                groups_lessons[group].append([key, set_elem])
                                free_time[group][size-1] = 1
        for group in groups_lessons:
            if len(groups_lessons[group]) < size:
                groups_lessons[group].append([0])

    return groups_lessons


def main():
    teachers = link_all_subjects()

    lessons = generate_all_lessons(teachers)

    schedule = generate_schedule(lessons)

    lessons_by_group = schedule_by_groups(schedule)
    xlsx.schedule_to_xlsx(lessons_by_group)


if __name__ == '__main__':
    main()
