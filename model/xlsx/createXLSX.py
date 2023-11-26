import enum

import xlsxwriter
import model.xlsx.formats as form


class Weekdays(enum.Enum):
    Monday = 'понедельник'
    Tuesday = 'вторник'
    Wednesday = 'среда'
    Thursday = 'четверг'
    Friday = 'пятница'
    Saturday = 'суббота'


class Clocks(enum.Enum):
    """Time of lessons"""
    first = '8.00-9.35'
    second = '9.55-11.30'
    third = '11.40-13.15'
    fourth = '13.55-15.30'


# Constants
days_of_study = len(Weekdays)
lessons_per_day = len(Clocks)

# Create formats
workbook = xlsxwriter.Workbook('../view/assets/xlsx/schedule.xlsx')

merge_format = workbook.add_format(form.Formats.get_merge_format())
merge_format_flip = workbook.add_format(form.Formats.get_merge_format_flip())
format_bot_cell = workbook.add_format(form.Formats.get_format_bot_cell())
format_top_cell = workbook.add_format(form.Formats.get_format_top_cell())


def markup(worksheet, data):
    """Makes the initial layout of the sheet

    Args:
        worksheet: The sheet to mark up
        data: A dict of data to mark up

    """
    worksheet.set_column(1, 30, 20)

    worksheet.merge_range(10, 0, 14, 0, 'День', merge_format)
    worksheet.merge_range(10, 1, 14, 1, 'Время', merge_format)

    row = 15
    column = 0
    for day in Weekdays:
        worksheet.merge_range(row, column, row + 4 * lessons_per_day - 1, column, day.value, merge_format_flip)
        row += 4 * lessons_per_day

    row = 15
    column = 1
    for _ in Weekdays:
        for time in Clocks:
            worksheet.merge_range(row, column, row + 3, column, time.value, merge_format)
            row += 4

    row = 10
    column = 2
    for cell in data:
        worksheet.merge_range(row, column, row + 4, column + 1, cell, merge_format)
        column += 2


def schedule_to_xlsx(groups, free_time, teachers):
    """Create schedule at xlsx
    
    Args:
        teachers: A dict mapped teacher's name and lesson.
        groups: A dict mapped group's number and array of subject's name and teacher's name.
        free_time: A dict mapped group's number and array of id of every lesson.

    """

    worksheet = workbook.add_worksheet('Groups schedule')

    markup(worksheet, groups)

    start_row = 15
    column = 2
    for group, lessons in groups.items():
        row = start_row
        day, num = 0, 0
        for index, lesson in enumerate(lessons):
            if day == 0:
                row = start_row + num * 4
                num += 1
            if lesson[0] != 0:
                curr_column = column - 1
                keys = groups.keys()
                key = iter(keys)
                q = next(key)
                while q != group:
                    q = next(key)
                while True:
                    if free_time[group][index] == free_time[q][index]:
                        curr_column += 2
                    else:
                        break
                    try:
                        q = next(key)
                    except StopIteration:
                        break

                try:
                    worksheet.merge_range(row, column, row + 1, curr_column, lesson[0], format_top_cell)
                    worksheet.merge_range(row + 2, column, row + 3, curr_column, lesson[1], format_bot_cell)
                except:
                    pass
            else:
                worksheet.merge_range(row, column, row + 1, column + 1, '', format_top_cell)
                worksheet.merge_range(row + 2, column, row + 3, column + 1, '', format_bot_cell)
            day += 1
            day %= days_of_study
            row += 4 * lessons_per_day
        column += 2

    worksheet = workbook.add_worksheet('Teachers schedule')

    markup(worksheet, teachers)

    row = 10
    column = 2

    for teacher, lessons in teachers.items():
        row = start_row
        day, num = 0, 0
        for index, lesson in enumerate(lessons):
            if day == 0:
                row = start_row + num * 4
                num += 1
            if lesson[0] != 0:
                worksheet.merge_range(row, column, row + 1, column + 1, lesson[0], format_top_cell)
                worksheet.merge_range(row + 2, column, row + 3, column + 1, lesson[1], format_bot_cell)
            else:
                worksheet.merge_range(row, column, row + 1, column + 1, '', format_top_cell)
                worksheet.merge_range(row + 2, column, row + 3, column + 1, '', format_bot_cell)
            day += 1
            day %= days_of_study
            row += 4 * lessons_per_day
        column += 2

    workbook.close()
