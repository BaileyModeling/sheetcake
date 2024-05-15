from sheetcake import Cell


def test_cell_gt():
    a = Cell(5)
    b = Cell(3)
    assert a > b
    assert not b > a


def test_cell_ge():
    a = Cell(5)
    b = Cell(3)
    assert a >= b
    assert not b >= a
    c = Cell(5)
    assert a >= c


def test_cell_lt():
    a = Cell(5)
    b = Cell(3)
    assert b < a
    assert not a < b


def test_cell_le():
    a = Cell(5)
    b = Cell(3)
    assert b <= a
    assert not a <= b
    c = Cell(5)
    assert a <= c


def test_cell_eq():
    a = Cell(5)
    b = Cell(3)
    assert not a == b
    c = Cell(5)
    assert a == c


def test_cell_ne():
    a = Cell(5)
    b = Cell(3)
    assert a != b
    c = Cell(5)
    assert not a != c
