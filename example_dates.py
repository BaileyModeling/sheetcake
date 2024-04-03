from sheetcake import DateCell, dates
from sheetcake.src.cells.date_cell import edays_cell, edate_cell, eomonth_cell, max_date_cell, min_date_cell, AbstractDateOperation
# from sheetcake.src.cells.date_cell import edays_cell
from datetime import date
import datetime


# a = DateCell(value=date(2024, 3, 1), name="Test Date 1")
# b = DateCell(name="Test Date 2")
# b.equal(a)
# a.value = date(2024, 12, 1)
# print(a.value)
# print(b.value)

# print(a.operation)
# print(b.operation)

# print(datetime.date(2024, 3, 1) == date(2024, 3, 1))

# a = DateCell(date(2024, 3, 1), "a")
# b = DateCell(name="b")
# b.edays(a, 5)
# a.value = date(2024, 12, 1)
# print(b.value)
# print(b.operations)

a = DateCell(date(2024, 1, 1), "a")
b = DateCell(date(2025, 1, 1), name="b")
c = DateCell(date(2026, 1, 1), name="c")
d = DateCell(date(2027, 1, 1), name="d")
e = max_date_cell(cells=[a, b, c, d], name="e")
print(e)
print(e.formula())
print(e.formula(deep=True))
# result = "edays( edays( a, 5 ), 5)"
