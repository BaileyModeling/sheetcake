from sheetcake2 import Cell
from sheetcake2.src.cells.cell import div_item, floordiv_item
import pytest


def test_cell_integer_division():
    a = Cell()
    a.equal(8)
    a.div(2)
    assert a.value == 4


def test_cell_division():
    a = Cell(8)
    b = Cell(2)
    c = Cell()
    c.add(a)
    c.div(b)
    assert c.value == 4


def test_cell_division_updates():
    a = Cell(10)
    b = Cell(3)
    c = Cell()
    c.add(a)
    c.div(b)
    a.value = 8
    b.value = 2
    assert c.value == 4


def test_cell_division_operator():
    a = Cell(8)
    b = Cell(2)
    c = a / b
    assert c.value == 4


def test_division_zero_cell_by_int_one():
    a = Cell(0)
    # c = a / 1
    c = Cell(a).div(1)
    assert c.value == 0


def test_division_by_zero_raises_exception():
    zero = Cell(0)
    one = Cell(1)
    with pytest.raises(Exception) as e_info:
        # c = one / zero
        c = Cell(one).div(zero)


def test_division_by_empty_cell_returns_None():
    empty = Cell()
    five = Cell(5)
    c = five / empty
    assert c.value is None


def test_empty_cell_division_returns_None():
    empty = Cell()
    five = Cell(5)
    c = empty / five
    assert c.value is None


def test_division_by_empty_cell_updates():
    a = Cell(10)
    b = Cell()
    c = a / b
    b.value = 2
    assert c.value == 5


def test_cell_division_updating_value_cascades_all_results():
    a = Cell(100, name='a')
    b = Cell(10, name='b')
    c = a / b
    d = Cell(5, name='d')
    e = c / d
    a.value = 200
    assert c.value == 20
    assert e.value == 4


def test_dividing_int_by_cell():
    a = Cell(10, name='a')
    c = 20 / a
    assert c.value == 2


def test_dividing_cell_by_int():
    a = Cell(20, name='a')
    c = a / 10
    assert c.value == 2
