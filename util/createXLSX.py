import xlsxwriter
import enum
from model.main import schedule_by_groups


class Weekdays(enum.Enum):

    Monday = 'monday'
    Tuesday = 'tuesday'
    Wednesday = 'wednesday'
    Thursday = 'thursday'
    Friday = 'friday'


class Clocks(enum.Enum):

    first = '8.00-8.45'
    second = '9.00-9.45'
    third = '9.55-10.40'
    fourth = '10.50-11.35'
    fifth = '11.45-12.30'


workbook = xlsxwriter.Workbook('schedule.xlsx')
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

worksheet.merge_range(10, 0, 14, 0, 'Days', merge_format)
worksheet.merge_range(10, 1, 14, 1, 'Time', merge_format)

row = 15
column = 0
for day in Weekdays:
    worksheet.merge_range(row, column, row + 19, column, day.value, merge_format_flip)
    row += 20

row = 15
column = 1
for day in Weekdays:
    for time in Clocks:
        worksheet.merge_range(row, column, row + 3, column, time.value, merge_format)
        row += 4

groups = schedule_by_groups()
print(groups)

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
            worksheet.merge_range(row, column, row + 3, column, lesson[0] + '\n' + lesson[1], merge_format)
        else:
            worksheet.merge_range(row, column, row + 3, column, '', merge_format)
        day += 1
        day %= 5
        row += 20
    column += 1


workbook.close()
