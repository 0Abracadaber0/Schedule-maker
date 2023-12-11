import enum

import xlsxwriter
import controller.xlsx.formats as form

from xlsxwriter.exceptions import OverlappingRange


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
workbook = xlsxwriter.Workbook('./schedules/schedule.xlsx')

merge_format = workbook.add_format(form.Formats.get_merge_format())
merge_format_flip = workbook.add_format(form.Formats.get_merge_format_flip())
merge_format_back_flip = workbook.add_format(form.Formats.get_merge_format_back_flip())

format_top_cell_lecture = workbook.add_format({**form.Formats.get_format_top_cell(), 'font_size': 20})
format_mid_cell_lecture = workbook.add_format({**form.Formats.get_format_mid_cell(), 'font_size': 20})
format_bot_cell_lecture = workbook.add_format({**form.Formats.get_format_bot_cell(), 'font_size': 20})

format_top_cell_practice = workbook.add_format(form.Formats.get_format_top_cell())
format_mid_cell_practice = workbook.add_format(form.Formats.get_format_mid_cell())
format_bot_cell_practice = workbook.add_format(form.Formats.get_format_bot_cell())

format_top_cell_lab = workbook.add_format({**form.Formats.get_format_top_cell(), 'font_size': 8})
format_mid_cell_lab = workbook.add_format({**form.Formats.get_format_mid_cell(), 'font_size': 8})
format_bot_cell_lab = workbook.add_format({**form.Formats.get_format_bot_cell(), 'font_size': 8})


def markup(worksheet, data):
    """Makes the initial layout of the sheet

    Args:
        worksheet: The sheet to mark up
        data: A dict of data to mark up

    """
    worksheet.set_column(1, 100, 20)
    worksheet.set_default_row(20)
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

    worksheet.merge_range(10, column, 14, column, 'Время', merge_format)
    worksheet.set_column(column + 1, column + 1, 10)
    worksheet.merge_range(10, column + 1, 14, column + 1, 'День', merge_format)

    row = 15
    for _ in Weekdays:
        for time in Clocks:
            worksheet.merge_range(row, column, row + 3, column, time.value, merge_format)
            row += 4

    row = 15
    column += 1
    for day in Weekdays:
        worksheet.merge_range(row, column, row + 4 * lessons_per_day - 1, column, day.value, merge_format_back_flip)
        row += 4 * lessons_per_day


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
        for i in range(2):
            day, num = 0, 0
            for index, lesson in enumerate(lessons):
                if day == 0:
                    row = start_row + num * lessons_per_day
                    num += 1
                if lesson[i][0] != 0:
                    curr_column = column

                    keys = groups.keys()
                    key = iter(keys)
                    q = next(key)
                    while q != group:
                        q = next(key)
                    # print(i, group, groups[group][index])
                    if i == 0:
                        if free_time[group][index][0] == free_time[group][index][1]:
                            curr_column += 1
                            flag = True
                            try:
                                q = next(key)
                            except StopIteration:
                                flag = False
                            while flag:
                                # print(curr_column, free_time[group][index], free_time[q][index])
                                if free_time[group][index] == free_time[q][index]:
                                    curr_column += 2
                                else:
                                    break
                                try:
                                    q = next(key)
                                except StopIteration:
                                    break

                        try:
                            if curr_column == column:
                                worksheet.merge_range(row, column, row + 1, curr_column, lesson[i][0],
                                                      format_top_cell_lab)
                                worksheet.write(row + 2, column, lesson[i][1], format_mid_cell_lab)
                                worksheet.write(row + 3, column, lesson[i][2], format_bot_cell_lab)
                            elif curr_column - column == 1:
                                worksheet.merge_range(row, column, row + 1, curr_column, lesson[i][0],
                                                      format_top_cell_practice)
                                worksheet.merge_range(row + 2, column, row + 2, curr_column, lesson[i][1],
                                                      format_mid_cell_practice)
                                worksheet.merge_range(row + 3, column, row + 3, curr_column, lesson[i][2],
                                                      format_bot_cell_practice)
                            else:
                                worksheet.merge_range(row, column, row + 1, curr_column, lesson[i][0],
                                                      format_top_cell_lecture)
                                worksheet.merge_range(row + 2, column, row + 2, curr_column, lesson[i][1],
                                                      format_mid_cell_lecture)
                                worksheet.merge_range(row + 3, column, row + 3, curr_column, lesson[i][2],
                                                      format_bot_cell_lecture)
                        except OverlappingRange:
                            ...

                    else:
                        if free_time[group][index][1] != free_time[group][index][0]:
                            try:
                                worksheet.merge_range(row, column, row + 1, column, lesson[i][0], format_top_cell_lab)
                                worksheet.write(row + 2, column, lesson[i][1], format_mid_cell_lab)
                                worksheet.write(row + 3, column, lesson[i][2], format_bot_cell_lab)
                            except OverlappingRange:
                                ...

                else:
                    try:
                        worksheet.merge_range(row, column, row + 1, column, '', format_top_cell_lab)
                        worksheet.merge_range(row + 2, column, row + 3, column, '', format_bot_cell_lab)
                    except OverlappingRange:
                        ...

                day += 1
                day %= days_of_study
                row += 4 * lessons_per_day
            column += 1

    worksheet = workbook.add_worksheet('Teachers schedule')

    markup(worksheet, teachers)

    column = 2

    for teacher, lessons in teachers.items():
        row = start_row
        day, num = 0, 0
        for index, lesson in enumerate(lessons):
            if day == 0:
                row = start_row + num * 4
                num += 1
            if lesson[0] != 0:
                worksheet.merge_range(row, column, row + 1, column + 1, lesson[0], format_top_cell_practice)
                worksheet.merge_range(row + 2, column, row + 2, column + 1, lesson[1], format_mid_cell_practice)
                worksheet.merge_range(row + 3, column, row + 3, column + 1, lesson[2], format_bot_cell_practice)
            else:
                worksheet.merge_range(row, column, row + 1, column + 1, '', format_top_cell_practice)
                worksheet.merge_range(row + 2, column, row + 3, column + 1, '', format_bot_cell_practice)
            day += 1
            day %= days_of_study
            row += 4 * lessons_per_day
        column += 2

    workbook.close()
