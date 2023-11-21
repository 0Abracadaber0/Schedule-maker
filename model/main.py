import random
from itertools import count
from faker import Faker
import model.xlsx.createXLSX as xlsx

# faker for generate teacher's names
faker = Faker()
names = (faker.name() for _ in count())


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

groups = {
    '10701122': 1,
    '10701222': 1,
    '10701322': 1,
    '10702122': 2,
    '10702222': 2,
    '10702322': 2,
    '10702422': 2
}

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

teachers = {}
all_lessons = []

free_time = {key: [0] * lessons_per_week for key in groups.keys()}

schedule = [[{0: {0, 0}}] * len(groups) for i in range(lessons_per_week)]


def generate_teacher():
    return next(name for name in names)


def link_all_subjects():
    for subject in subjects:
        teachers.update({subject: [generate_teacher() for _ in range(subjects.get(subject))]})


def generate_all_lessons():
    for group in groups:
        lessons = plans.get(groups.get(group))
        for lesson in lessons:
            teacher = random.choice(teachers[lesson])
            for i in range(lessons.get(lesson)[1]):
                all_lessons.append({lesson: {group, teacher}})
    print(all_lessons)


def generate_schedule():
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


def schedule_by_groups():
    # print(schedule)

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
    link_all_subjects()
    generate_all_lessons()
    generate_schedule()

    lessons_by_group = schedule_by_groups()
    xlsx.schedule_to_xlsx(lessons_by_group)


if __name__ == '__main__':
    main()
