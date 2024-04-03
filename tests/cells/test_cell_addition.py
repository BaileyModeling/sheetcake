from sheetcake2 import Cell
from decimal import Decimal


def test_blank_cell_integer_addition():
    a = Cell()
    a.add(5)
    assert a.value == 5
    a.add(3)
    assert a.value == 8


def test_cell_integer_addition():
    a = Cell()
    a.equal(5)
    assert a.value == 5
    a.add(3)
    assert a.value == 8


def test_cell_addition_operator():
    a = Cell(5)
    b = Cell(3)
    c = a + b
    assert c.value == 8


def test_cell_addition():
    a = Cell(3)
    b = Cell(4)
    c = Cell()
    c.add(a)
    c.add(b)
    assert c.value == 7


def test_cell_addition_updates():
    a = Cell(3)
    b = Cell(4)
    c = Cell()
    c.add(a)
    c.add(b)
    b.value = 5
    assert c.value == 8


def test_sum_multiple_cells():
    a = Cell(3)
    b = Cell(4)
    c = Cell(5)
    d = sum((a, b, c))
    assert d.value == 12


def test_sum_array_of_cells():
    a = Cell(9, name="a")
    previous = a
    cells = []
    for _ in range(100):
        cell = Cell(previous)
        cells.append(cell)
        previous = cell
    total = sum(cells)
    a.value = 1
    assert total.value == 100


def test_addition_of_int_and_cell():
    c = 5 + Cell(3)
    assert c.value == 8


def test_addition_of_cell_and_int():
    c = Cell(3) + 5
    assert c.value == 8


def test_cell_int_addition_does_not_update():
    a = 5
    b = Cell(3)
    c = b + a
    a = 99
    assert c.value == 8


def test_cell_int_addition_does_update():
    a = 5
    b = Cell(3)
    c = b + a
    b.value = 10
    assert c.value == 15


def test_cell_and_decimal_addition():
    a = Cell(5)
    b = Decimal(3)
    c = a + b
    assert c.value == 8