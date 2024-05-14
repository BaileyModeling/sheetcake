from sheetcake import DateCell, CountDaysCell
from datetime import date
import pytest
from typing import List


def test_count_days_cell_init():
    start = DateCell(date(2023, 1, 1), name="b")
    end = DateCell(date(2024, 1, 1), name="c")
    days = CountDaysCell(start, end, name="days")
    assert days.value == 365


def test_count_days_cell_end_date_updates():
    start = DateCell(date(2023, 1, 1), name="b")
    end = DateCell(date(2024, 1, 1), name="c")
    days = CountDaysCell(start, end, name="days")
    end.value = date(2024, 1, 2)
    assert days.value == 366


def test_count_days_cell_start_date_updates():
    start = DateCell(date(2023, 1, 1), name="b")
    end = DateCell(date(2024, 1, 1), name="c")
    days = CountDaysCell(start, end, name="days")
    start.value = date(2023, 12, 31)
    assert days.value == 1


def test_count_days_cell_cannot_change_value():
    start = DateCell(date(2023, 1, 1), name="b")
    end = DateCell(date(2024, 1, 1), name="c")
    days = CountDaysCell(start, end, name="days")
    days.value = 100
    assert days.value == 365
