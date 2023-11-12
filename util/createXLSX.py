import xlsxwriter
import enum
from model.main import schedule_by_groups


class Weekdays(enum.Enum):

    Monday = 'понедельник'
    Tuesday = 'вторник'
    Wednesday = 'среда'
    Thursday = 'четверг'
    Friday = 'пятница'


class Clocks(enum.Enum):

    first = '8.00-9.35'
    second = '9.55-11.30'
    third = '11.40-13.15'
    fourth = '13.55-15.30'
    fifth = '15.40-17.15'


workbook = xlsxwriter.Workbook('schedule.xlsx')
worksheet = workbook.add_worksheet()

worksheet.set_column(1, 14, 18)

merge_format_flip = workbook.add_format({
    'font_size': 20,
    'align':     'center',
    'valign':    'vcenter',
    'rotation':  90
})

merge_format = workbook.add_format({
    'font_size': 15,
    'align':     'center',
    'valign':    'vcenter'
})

worksheet.merge_range(10, 0, 14, 0, 'Дни', merge_format)
worksheet.merge_range(10, 1, 14, 1, 'Часы', merge_format)

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
for group, lessons in groups.items():
    worksheet.merge_range(row, column, row + 4, column, group, merge_format)
    column += 1


workbook.close()
