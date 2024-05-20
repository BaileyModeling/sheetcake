from sheetcake import DateCell
from datetime import date


def test_date_cell_eq_date():
    cell = DateCell(value=date(2024, 3, 1), name="Test Date")
    assert cell == date(2024, 3, 1)


def test_date_cell_eq_date_cell():
    a = DateCell(value=date(2024, 3, 1), name="Test Date 1")
    b = DateCell(value=date(2024, 3, 1), name="Test Date 2")
    assert a == b


def test_date_cell_gt():
    a = DateCell(date(2024, 3, 1), "a")
    b = DateCell(date(2024, 2, 1), "b")
    assert a > b
    assert not a < b


def test_date_cell_ge():
    a = DateCell(date(2024, 3, 1), "a")
    b = DateCell(date(2024, 2, 1), "b")
    c = DateCell(date(2024, 3, 1), "c")
    assert a >= b
    assert not b >= a
    assert a >= c


def test_date_cell_gt_date():
    a = DateCell(date(2024, 3, 1), "a")
    b = date(2024, 2, 1)
    assert a > b
    assert not b > a


def test_date_cell_ge_date():
    a = DateCell(date(2024, 3, 1), "a")
    b = date(2024, 2, 1)
    c = date(2024, 3, 1)
    assert a >= b
    assert not b >= a
    assert a >= c


def test_date_cell_gt_date_rev():
    a = date(2024, 3, 1)
    b = DateCell(date(2024, 2, 1), "b")
    assert a > b
    assert not b > a


def test_date_cell_gt_date_false():
    a = date(2024, 3, 1)
    b = DateCell(date(2024, 2, 1), "b")
    assert not a < b


def test_date_cell_lt():
    a = DateCell(date(2024, 2, 1), "a")
    b = DateCell(date(2024, 3, 1), "b")
    assert a < b
    assert not b < a


def test_date_cell_le():
    a = DateCell(date(2024, 2, 1), "a")
    b = DateCell(date(2024, 3, 1), "b")
    c = DateCell(date(2024, 2, 1), "c")
    assert a <= b
    assert not b <= a
    assert a <= c


def test_date_cell_lt_date():
    a = DateCell(date(2024, 2, 1), "a")
    b = date(2024, 3, 1)
    assert a < b


def test_date_cell_le_date():
    a = DateCell(date(2024, 2, 1), "a")
    b = date(2024, 3, 1)
    c = date(2024, 2, 1)
    assert a <= b
    assert not b <= a
    assert a <= c


def test_date_cell_lt_date_rev():
    a = date(2024, 2, 1)
    b = DateCell(date(2024, 3, 1), "b")
    assert a < b


def test_date_cell_lt_date_false():
    a = date(2024, 2, 1)
    b = DateCell(date(2024, 3, 1), "b")
    assert not a > b


def test_date_cell_is_after():
    a = DateCell(date(2024, 3, 1), "a")
    b = DateCell(date(2024, 2, 1), "b")
    assert a.is_after(b)
    assert not b.is_after(a)


def test_date_cell_is_after_date():
    a = DateCell(date(2024, 3, 1), "a")
    b = date(2024, 2, 1)
    assert a.is_after(b)


def test_date_cell_is_after_inclusive():
    a = DateCell(date(2024, 3, 1), "a")
    b = DateCell(date(2024, 3, 1), "b")
    assert a.is_after(b, inclusive=True)
    assert b.is_after(a, inclusive=True)


def test_date_cell_is_before():
    a = DateCell(date(2024, 2, 1), "a")
    b = DateCell(date(2024, 3, 1), "b")
    assert a.is_before(b)
    assert not b.is_before(a)


def test_date_cell_is_before_date():
    a = DateCell(date(2024, 2, 1), "a")
    b = date(2024, 3, 1)
    assert a.is_before(b)


def test_date_cell_is_before_inclusive():
    a = DateCell(date(2024, 3, 1), "a")
    b = DateCell(date(2024, 3, 1), "b")
    assert a.is_before(b, inclusive=True)
    assert b.is_before(a, inclusive=True)


def test_date_cell_is_between():
    a = DateCell(date(2024, 1, 1), "a")
    b = DateCell(date(2024, 2, 1), "b")
    c = DateCell(date(2024, 3, 1), "c")
    assert b.is_between(a, c)
    assert not a.is_between(b, c)
    assert not c.is_between(a, b)


def test_date_cell_is_between_incl_start():
    a = DateCell(date(2024, 1, 1), "a")
    b = DateCell(date(2024, 1, 1), "b")
    c = DateCell(date(2024, 3, 1), "c")
    assert b.is_between(a, c, incl_start=True)
    assert not b.is_between(a, c, incl_start=False)


def test_date_cell_is_between_incl_end():
    a = DateCell(date(2024, 1, 1), "a")
    b = DateCell(date(2024, 3, 1), "b")
    c = DateCell(date(2024, 3, 1), "c")
    assert b.is_between(a, c, incl_end=True)
    assert not b.is_between(a, c, incl_end=False)


def test_date_cell_is_between_incl_start_incl_end():
    a = DateCell(date(2024, 1, 1), "a")
    b = DateCell(date(2024, 1, 1), "b")
    c = DateCell(date(2024, 3, 1), "c")
    d = DateCell(date(2024, 3, 1), "d")
    assert b.is_between(a, c, incl_start=True, incl_end=True)
    assert d.is_between(a, c, incl_start=True, incl_end=True)
    assert not b.is_between(a, c, incl_start=False, incl_end=True)
    assert not d.is_between(a, c, incl_start=True, incl_end=False)
    assert not b.is_between(a, c, incl_start=False, incl_end=False)
    assert not d.is_between(a, c, incl_start=False, incl_end=False)


def test_date_cell_is_between_dates():
    a = date(2024, 1, 1)
    b = DateCell(date(2024, 2, 1), "b")
    c = date(2024, 3, 1)
    assert b.is_between(a, c)
