from sheetcake import DateCell, errors, validation_rules, Cell
from sheetcake.src.cells.date_cell import edays_cell, edate_cell, eomonth_cell, max_date_cell, min_date_cell, AbstractDateOperation
from datetime import date
import pytest
from typing import List
from types import SimpleNamespace


def test_date_cell_eomonth_operation():
    a = DateCell(date(2024, 3, 1), "a")
    b = DateCell(name="b")
    b.eomonth_item(a, 5)
    assert b.value == date(2024, 8, 31)


def test_eomonth_cell():
    a = DateCell(date(2024, 3, 1), "a")
    b = eomonth_cell(a, 5, name="b")
    assert b.value == date(2024, 8, 31)


def test_eomonth_cell_dynamic_months():
    a = DateCell(date(2024, 3, 1), "a")
    months = Cell(5)
    b = eomonth_cell(a, months, name="b")
    assert b.value == date(2024, 8, 31)


def test_eomonth_cell_dynamic_months_updates():
    a = DateCell(date(2024, 3, 1), "a")
    months = Cell(5)
    b = eomonth_cell(a, months, name="b")
    months.value = 6
    assert b.value == date(2024, 9, 30)


def test_date_cell_eomonth_operation_updates():
    a = DateCell(date(2024, 3, 1), "a")
    b = DateCell(name="b")
    b.eomonth_item(a, 5)
    a.value = date(2024, 1, 1)
    assert b.value == date(2024, 6, 30)


def test_date_cell_eomonth_operation_consecutive():
    a = DateCell(date(2024, 1, 1), "a")
    b = DateCell(name="b")
    b.eomonth_item(a, 5)
    b.eomonth_item(None, 5)
    assert b.value == date(2024, 11, 30)


def test_date_cell_eomonth_formula():
    a = DateCell(date(2024, 3, 1), "a")
    b = DateCell(name="b")
    b.eomonth_item(a, 5)
    assert b.formula() == "eomonth( a, 5 )"


def test_date_cell_eomonth_formula_deep():
    a = DateCell(date(2024, 3, 1), "a")
    b = DateCell(a, name="b")
    c = DateCell(name="c")
    c.eomonth_item(a, 5)
    assert c.formula(deep=True) == "eomonth( 2024-03-01, 5 )"


def test_date_cell_eomonth_formula_date():
    a = date(2024, 3, 1)
    b = DateCell(name="b")
    b.eomonth_item(a, 5)
    assert b.formula() == "eomonth( 2024-03-01, 5 )"


def test_date_cell_eomonth_value_audit():
    a = DateCell(date(2024, 3, 1), "a")
    b = DateCell(name="b")
    b.eomonth_item(a, 5)
    assert b.value_audit() == "eomonth( 2024-03-01, 5 )"


def test_date_cell_eomonth_value_audit_deep():
    a = DateCell(date(2024, 3, 1), "a")
    b = DateCell(a, name="b")
    c = DateCell(name="c")
    c.eomonth_item(a, 5)
    assert c.value_audit(deep=True) == "eomonth( 2024-03-01, 5 )"
