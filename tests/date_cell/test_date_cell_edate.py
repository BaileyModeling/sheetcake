from sheetcake import DateCell, Cell
from sheetcake.src.cells.date_cell import edate_cell
from datetime import date
import pytest
from typing import List


def test_date_cell_edate_operation():
    a = DateCell(date(2024, 3, 1), "a")
    b = DateCell(name="b")
    b.edate_item(a, 5)
    assert b.value == date(2024, 8, 1)


def test_edate_cell():
    a = DateCell(date(2024, 3, 1), "a")
    b = edate_cell(a, 5, name="b")
    assert b.value == date(2024, 8, 1)


def test_date_cell_edate_operation_updates():
    a = DateCell(date(2024, 3, 1), "a")
    b = DateCell(name="b")
    b.edate_item(a, 5)
    a.value = date(2024, 1, 1)
    assert b.value == date(2024, 6, 1)


def test_date_cell_edate_operation_consecutive():
    a = DateCell(date(2024, 1, 1), "a")
    b = DateCell(name="b")
    b.edate_item(a, 5)
    b.edate_item(None, 5)
    assert b.value == date(2024, 11, 1)


def test_edate_dynamic_months():
    a = DateCell(date(2024, 3, 1), "a")
    months = Cell(5)
    b = edate_cell(a, months, name="b")
    assert b.value == date(2024, 8, 1)


def test_edate_dynamic_months_updates():
    a = DateCell(date(2024, 3, 1), "a")
    months = Cell(5)
    b = edate_cell(a, months, name="b")
    months.value = 6
    assert b.value == date(2024, 9, 1)


def test_date_cell_edate_formula():
    a = DateCell(date(2024, 3, 1), "a")
    b = DateCell(name="b")
    b.edate_item(a, 5)
    assert b.formula() == "edate( a, 5 )"


def test_date_cell_edate_formula_deep():
    a = DateCell(date(2024, 3, 1), "a")
    b = DateCell(a, name="b")
    c = DateCell(name="c")
    c.edate_item(a, 5)
    assert c.formula(deep=True) == "edate( 2024-03-01, 5 )"


def test_date_cell_edate_formula_date():
    a = date(2024, 3, 1)
    b = DateCell(name="b")
    b.edate_item(a, 5)
    assert b.formula() == "edate( 2024-03-01, 5 )"


def test_date_cell_edate_value_audit():
    a = DateCell(date(2024, 3, 1), "a")
    b = DateCell(name="b")
    b.edate_item(a, 5)
    assert b.value_audit() == "edate( 2024-03-01, 5 )"


def test_date_cell_edate_value_audit_deep():
    a = DateCell(date(2024, 3, 1), "a")
    b = DateCell(a, name="b")
    c = DateCell(name="c")
    c.edate_item(a, 5)
    assert c.value_audit(deep=True) == "edate( 2024-03-01, 5 )"
