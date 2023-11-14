import enum

import xlsxwriter


class Weekdays(enum.Enum):

    Monday = 'понедельник'
    Tuesday = 'вторник'
    Wednesday = 'среда'
    Thursday = 'четверг'
    Friday = 'пятница'
    Saturday = 'суббота'


class Clocks(enum.Enum):
    first = '8.00-9.35'
    second = '9.55-11.30'
    third = '11.40-13.15'
    fourth = '13.55-15.30'


days_of_study = len(Weekdays)
lessons_per_day = len(Clocks)


def schedule_to_xlsx(groups):
    print(lessons_per_day)
    workbook = xlsxwriter.Workbook('../view/assets/xlsx/schedule.xlsx')
    worksheet = workbook.add_worksheet()

    worksheet.set_column(1, 14, 30)

    merge_format_flip = workbook.add_format({
        'font_size': 20,
        'border':    5,
        'align':     'center',
        'valign':    'vcenter',
        'rotation':  90
    })

    merge_format = workbook.add_format({
        'font_size': 15,
        'border':    5,
        'align':     'center',
        'valign':    'vcenter'
    })

    merge_format_lesson = workbook.add_format({
        'font_size': 10,
        'top':       5,
        'left':      5,
        'right':     5,
        'align':     'center',
        'valign':    'vcenter'
    })

    merge_format_teacher = workbook.add_format({
        'font_size': 15,
        'bottom':    5,
        'left':      5,
        'right':     5,
        'align':     'center',
        'valign':    'vcenter'
    })

    worksheet.merge_range(10, 0, 14, 0, 'День', merge_format)
    worksheet.merge_range(10, 1, 14, 1, 'Время', merge_format)

    row = 15
    column = 0
    for day in Weekdays:
        worksheet.merge_range(row, column, row + 4*lessons_per_day-1, column, day.value, merge_format_flip)
        row += 4*lessons_per_day

    row = 15
    column = 1
    for _ in Weekdays:
        for time in Clocks:
            worksheet.merge_range(row, column, row + 3, column, time.value, merge_format)
            row += 4

    row = 10
    column = 2
    for group, _ in groups.items():
        worksheet.merge_range(row, column, row + 4, column, group, merge_format)
        column += 1

    start_row = 15
    column = 2
    for group, lessons in groups.items():
        row = start_row
        day, num = 0, 0
        for lesson in lessons:
            if day == 0:
                row = start_row + num * 4
                num += 1
            if lesson[0] != 0:
                worksheet.merge_range(row, column, row + 1, column, lesson[0], merge_format_lesson)
                worksheet.merge_range(row + 2, column, row + 3, column, lesson[1], merge_format_teacher)
            else:
                worksheet.merge_range(row, column, row + 1, column, '', merge_format_lesson)
                worksheet.merge_range(row + 2, column, row + 3, column, '', merge_format_teacher)
            day += 1
            day %= days_of_study
            row += 4*lessons_per_day
        column += 1

    workbook.close()
