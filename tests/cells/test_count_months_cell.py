from sheetcake import DateCell, CountMonthsCell
from datetime import date
import pytest
from typing import List


def test_count_months_cell_init():
    start = DateCell(date(2023, 1, 1), name="b")
    end = DateCell(date(2024, 1, 1), name="c")
    months = CountMonthsCell(start, end, name="months")
    assert months.value == 12


def test_count_months_cell_end_date_updates():
    start = DateCell(date(2023, 1, 1), name="b")
    end = DateCell(date(2024, 1, 1), name="c")
    months = CountMonthsCell(start, end, name="months")
    end.value = date(2024, 2, 1)
    assert months.value == 13


def test_count_months_cell_start_date_updates():
    start = DateCell(date(2023, 1, 1), name="b")
    end = DateCell(date(2024, 1, 1), name="c")
    months = CountMonthsCell(start, end, name="months")
    start.value = date(2023, 12, 31)
    assert months.value == 1


def test_count_months_cell_cannot_change_value():
    start = DateCell(date(2023, 1, 1), name="b")
    end = DateCell(date(2024, 1, 1), name="c")
    months = CountMonthsCell(start, end, name="months")
    months.value = 100
    assert months.value == 12
