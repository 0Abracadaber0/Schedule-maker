import random
from itertools import count
from faker import Faker

faker = Faker()

names = (faker.name() for _ in count())

subjects = {
    'English': 1,
    'math': 1,
    'art': 1,
    'science': 1,
    'history': 1,
    'music': 1,
    'geography': 1,
    'P.E.': 1,
    'I.T.': 1,
    'biology': 1
}

groups = {
    '11A': 11,
    '11B': 11,
    '11C': 11,
    '11D': 11,
    '9B': 9,
    '9C': 9
}

plans = {
    11: {'English': 3, 'math': 4, 'science': 3, 'geography': 2, 'I.T.': 2, 'biology': 2},
    9: {'English': 2, 'math': 3, 'art': 1, 'history': 2, 'music': 1, 'P.E.': 2, 'biology': 2}
}

lessons_per_week = 40

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


link_all_subjects()

generate_all_lessons()


generate_schedule()
# print(schedule)

monday = []
tuesday = []
wednesday = []
thursday = []
friday = []

for index, row in enumerate(schedule):
    match index % 5:
        case 0:
            monday.append(row)
        case 1:
            tuesday.append(row)
        case 2:
            wednesday.append(row)
        case 3:
            thursday.append(row)
        case 4:
            friday.append(row)

print(monday)