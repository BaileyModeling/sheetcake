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


def test_max_date_cell():
    a = DateCell(date(2000, 1, 1), "a")
    b = DateCell(date(2024, 1, 1), "b")
    c = DateCell(date(2025, 1, 1), "c")
    d = DateCell.max([a, b, c], name="d")
    assert d.value == date(2025, 1, 1)


def test_date_cell_max_formula(cell_list: List[DateCell]):
    e = DateCell.max(cells=cell_list, name="e")
    assert e.formula() == "max( a, b, c, d )"


def test_date_cell_max_formula_deep(cell_list: List[DateCell]):
    e = DateCell.max(cells=cell_list, name="e")
    assert e.formula(deep=True) == "max( 2024-01-01, 2025-01-01, 2026-01-01, 2027-01-01 )"


def test_date_cell_max_value_audit(cell_list: List[DateCell]):
    e = DateCell.max(cells=cell_list, name="e")
    assert e.value_audit() == "max( a, b, c, d )"


def test_date_cell_max_value_audit_deep(cell_list: List[DateCell]):
    e = DateCell.max(cells=cell_list, name="e")
    assert e.value_audit(deep=True) == "max( 2024-01-01, 2025-01-01, 2026-01-01, 2027-01-01 )"


def test_date_cell_max_operation():
    a = DateCell(date(2000, 1, 1), "a")
    b = DateCell(date(2024, 1, 1), "b")
    c = DateCell(date(2025, 1, 1), "c")
    d = DateCell(name="d")
    d.max_items([a, b, c])
    assert d.value == date(2025, 1, 1)


def test_date_cell_max_operation_updates():
    a = DateCell(date(2000, 1, 1), "a")
    b = DateCell(date(2024, 1, 1), "b")
    c = DateCell(date(2025, 1, 1), "c")
    d = DateCell(name="d")
    d.max_items([a, b, c])
    a.value = date(2030, 1, 1)
    assert d.value == date(2030, 1, 1)


def test_date_cell_max_operation_consecutive():
    a = DateCell(date(2000, 1, 1), "a")
    b = DateCell(date(2024, 1, 1), "b")
    c = DateCell(date(2025, 1, 1), "c")
    d = DateCell(date(2026, 1, 1), "d")
    f = DateCell(date(2027, 1, 1), "f")
    g = DateCell(name="g")
    g.max_items([a, b, c])
    g.max_items([d, f])
    assert g.value == date(2027, 1, 1)

