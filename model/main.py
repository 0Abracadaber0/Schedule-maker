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
    'Алгоритмы и структуры данных': 1,
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
        'math': [1, 2],
        'science': [1, 3],
        'geography': [1, 1],
        'I.T.': [1, 1],
        'biology': [1, 1]
    },
    2: {
        'Алгоритмы и структуры данных': [1, 1],
        'math': [1, 2],
        'art': [1, 1],
        'history': [1, 1],
        'music': [1, 1],
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

            for i in range(plans[stream][lesson][0]):
                all_lessons.append({lesson: [stream, teacher]})

    for group in groups:
        lessons = plans.get(groups.get(group))
        for lesson in lessons:
            teacher = random.choice(teachers[lesson])
            for i in range(lessons.get(lesson)[1]):
                all_lessons.append({lesson: [group, teacher]})

    return all_lessons


def generate_schedule(all_lessons):
    """Distributes lessons in such a way that groups and teachers do not overlap at the same time.

    Args:
        all_lessons: A list of unique lessons.

    Returns: A dict mapped group's number and array of subject's name and teacher's name.
             For example:

             {
                '10701122': [['math', 'James Walters'], ['math', 'James Walters'], [0]],
                '10701222': [['science', 'Charles Farmer'], [0], [0]]
             }
    """
    # 0 - time is free, 1 - time isn't free
    free_time = {key: [0] * lessons_per_week for key in groups.keys()}

    schedule = {key: [[0, 0] for _ in range(lessons_per_week)] for key in groups.keys()}

    for i in range(lessons_per_week):
        for stream in plans.keys():
            for lesson in all_lessons:

                if lesson[list(lesson.keys())[0]][0] != stream:
                    continue

                flag = True
                for key in schedule.keys():
                    if schedule[key][i][1] == lesson[list(lesson.keys())[0]][1]:
                        flag = False

                        break

                if flag:
                    for group in groups.keys():
                        if groups[group] == stream:
                            free_time[group][i] = 1

                            schedule[group][i][0] = list(lesson.keys())[0]
                            schedule[group][i][1] = list(lesson.values())[0][1]

                            print('accepted:', group, schedule[group][i])

                    all_lessons.remove(lesson)

                    break

                else:
                    print('nope:', list(lesson.keys())[0], list(lesson.values())[0][1])

    for i in range(lessons_per_week):
        for group in schedule:
            if free_time[group][i] == 1:
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
                    free_time[group][i] = 1

                    schedule[group][i][0] = list(lesson.keys())[0]
                    schedule[group][i][1] = list(lesson.values())[0][1]

                    print('accepted:', group, schedule[group][i])

                    all_lessons.remove(lesson)

                    break

                else:
                    print('nope:', list(lesson.keys())[0], list(lesson.values())[0][1])

    print(free_time)
    return schedule


def main():
    teachers = link_all_subjects()

    lessons = generate_all_lessons(teachers)

    schedule = generate_schedule(lessons)

    xlsx.schedule_to_xlsx(schedule)


if __name__ == '__main__':
    main()
