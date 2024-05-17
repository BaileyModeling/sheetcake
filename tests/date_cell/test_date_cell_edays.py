from sheetcake import DateCell, errors, validation_rules, Cell
from sheetcake.src.cells.date_cell import edays_cell, edate_cell, eomonth_cell, max_date_cell, min_date_cell, AbstractDateOperation
from datetime import date
import pytest
from typing import List
from types import SimpleNamespace


def test_date_cell_edays_operation():
    a = DateCell(date(2024, 3, 1), "a")
    b = DateCell(name="b")
    b.edays_item(a, 5)
    assert b.value == date(2024, 3, 6)


def test_date_cell_edays_operation_consecutive():
    a = DateCell(date(2024, 3, 1), "a")
    b = DateCell(name="b")
    b.edays_item(a, 5)
    b.edays_item(None, 5)
    assert b.value == date(2024, 3, 11)


def test_edays_cell():
    a = DateCell(date(2024, 3, 1), "a")
    b = edays_cell(a, 5, name="b")
    a.value = date(2024, 12, 1)
    assert b.value == date(2024, 12, 6)


def test_edays_cell_dynamic_days():
    a = DateCell(date(2024, 3, 1), "a")
    days = Cell(5)
    b = edays_cell(a, days, name="b")
    a.value = date(2024, 12, 1)
    assert b.value == date(2024, 12, 6)


def test_edays_cell_dynamic_days_updates():
    a = DateCell(date(2024, 3, 1), "a")
    days = Cell(5)
    b = edays_cell(a, days, name="b")
    a.value = date(2024, 12, 1)
    days.value = 6
    assert b.value == date(2024, 12, 7)


def test_date_cell_edays_formula():
    a = DateCell(date(2024, 3, 1), "a")
    b = DateCell(name="b")
    b.edays_item(a, 5)
    assert b.formula() == "edays( a, 5 )"


def test_date_cell_edays_formula_deep():
    a = DateCell(date(2024, 3, 1), "a")
    b = DateCell(a, name="b")
    c = DateCell(name="c")
    c.edays_item(a, 5)
    assert c.formula(deep=True) == "edays( 2024-03-01, 5 )"


def test_date_cell_edays_value_audit():
    a = DateCell(date(2024, 3, 1), "a")
    b = DateCell(name="b")
    b.edays_item(a, 5)
    assert b.value_audit() == "edays( 2024-03-01, 5 )"


def test_date_cell_edays_value_audit_deep():
    a = DateCell(date(2024, 3, 1), "a")
    b = DateCell(a, name="b")
    c = DateCell(name="c")
    c.edays_item(a, 5)
    assert c.value_audit(deep=True) == "edays( 2024-03-01, 5 )"

