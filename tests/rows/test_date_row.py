from sheetcake2 import DateRow
from datetime import date


def test_date_row_get_value():
    row = DateRow.from_values([date(2022, 1, 1), date(2022, 1, 2)], "test")
    assert row.get_value(0) == date(2022, 1, 1)
    assert row.get_value(1) == date(2022, 1, 2)


def test_date_row_get_item():
    row = DateRow.from_values([date(2022, 1, 1), date(2022, 1, 2)], "test")
    assert row[0] == date(2022, 1, 1)
    assert row[1] == date(2022, 1, 2)


def test_date_row_len():
    row = DateRow.from_values([date(2022, 1, 1), date(2022, 1, 2)], "test")
    assert len(row) == 2


def test_date_row_iter():
    row = DateRow.from_values([date(2022, 1, 1), date(2022, 1, 2)], "test")
    assert list(row) == [date(2022, 1, 1), date(2022, 1, 2)]


def test_date_row_append():
    row = DateRow.from_values([date(2022, 1, 1), date(2022, 1, 2)], "test")
    row.append(date(2022, 1, 3))
    assert row[2] == date(2022, 1, 3)


def test_date_row_blank():
    row = DateRow.blank(2, "test")
    assert len(row) == 2
    assert row[0].value is None
