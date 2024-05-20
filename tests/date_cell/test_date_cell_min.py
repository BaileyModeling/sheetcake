from sheetcake import DateCell
from datetime import date
import pytest
from typing import List


@pytest.fixture
def cell_list() -> List[DateCell]:
    a = DateCell(date(2024, 1, 1), "a")
    b = DateCell(date(2025, 1, 1), "b")
    c = DateCell(date(2026, 1, 1), "c")
    d = DateCell(date(2027, 1, 1), "d")
    return [a, b, c, d]


def test_min_date_cell():
    a = DateCell(date(2000, 1, 1), "a")
    b = DateCell(date(2024, 1, 1), "b")
    c = DateCell(date(2025, 1, 1), "c")
    d = DateCell.min([a, b, c], name="d")
    assert d.value == date(2000, 1, 1)


def test_date_cell_min_formula(cell_list: List[DateCell]):
    e = DateCell.min(cells=cell_list, name="e")
    assert e.formula() == "min( a, b, c, d )"


def test_date_cell_min_formula_deep(cell_list: List[DateCell]):
    e = DateCell.min(cells=cell_list, name="e")
    assert e.formula(deep=True) == "min( 2024-01-01, 2025-01-01, 2026-01-01, 2027-01-01 )"


def test_date_cell_min_formula_with_date(cell_list: List[DateCell]):
    cell_list[0] = date(2024, 1, 1)
    e = DateCell.min(cells=cell_list, name="e")
    assert e.formula() == "min( 2024-01-01, b, c, d )"


def test_date_cell_min_value_audit(cell_list: List[DateCell]):
    e = DateCell.min(cells=cell_list, name="e")
    assert e.value_audit() == "min( a, b, c, d )"


def test_date_cell_min_value_audit_deep(cell_list: List[DateCell]):
    e = DateCell.min(cells=cell_list, name="e")
    assert e.value_audit(deep=True) == "min( 2024-01-01, 2025-01-01, 2026-01-01, 2027-01-01 )"


def test_date_cell_min_operation():
    a = DateCell(date(2000, 1, 1), "a")
    b = DateCell(date(2024, 1, 1), "b")
    c = DateCell(date(2025, 1, 1), "c")
    d = DateCell(name="d")
    d.min_items([a, b, c])
    assert d.value == date(2000, 1, 1)


def test_date_cell_min_operation_updates():
    a = DateCell(date(2000, 1, 1), "a")
    b = DateCell(date(2024, 1, 1), "b")
    c = DateCell(date(2025, 1, 1), "c")
    d = DateCell(name="d")
    d.min_items([a, b, c])
    a.value = date(1999, 1, 1)
    assert d.value == date(1999, 1, 1)


def test_date_cell_min_operation_consecutive():
    a = DateCell(date(2000, 1, 1), "a")
    b = DateCell(date(2024, 1, 1), "b")
    c = DateCell(date(2025, 1, 1), "c")
    d = DateCell(date(2026, 1, 1), "d")
    f = DateCell(date(2027, 1, 1), "f")
    g = DateCell(name="g")
    g.min_items([a, b, c])
    g.min_items([d, f])
    assert g.value == date(2000, 1, 1)
