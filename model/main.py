import random
from itertools import count
from faker import Faker
import model.xlsx.createXLSX as xlsx


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
    1: {'Алгоритмы и структуры данных': 3, 'math': 4, 'science': 3, 'geography': 2, 'I.T.': 2, 'biology': 2},
    2: {'Алгоритмы и структуры данных': 2, 'math': 3, 'art': 1, 'history': 2, 'music': 1, 'P.E.': 2, 'biology': 2}
}

lessons_per_week = xlsx.days_of_study * xlsx.lessons_per_day

teachers = {}
all_lessons = []

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
            for i in range(lessons.get(lesson)):
                all_lessons.append({lesson: {group, teacher}})


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
                            if group != set_elem:
                                groups_lessons[group].append([key, set_elem])
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
