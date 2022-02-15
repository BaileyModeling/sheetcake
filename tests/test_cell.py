from sheetcake import Cell


def test_cell_init_zero():
    cell = Cell(0)
    assert cell.value == 0
    assert isinstance(cell.value, int)


def test_cell_value_updates():
    cell = Cell()
    assert cell.value is None
    cell.value = 5
    assert cell.value == 5


def test_cell_init_with_another_cell_sets_value():
    a = Cell(5)
    b = Cell(a)
    assert b.value == 5


def test_cell_init_with_another_cell_updates():
    a = Cell(5)
    b = Cell(a)
    a.value = 3
    assert b.value == 3


def test_blank_cell_integer_multiplication():
    a = Cell()
    a.mult(5)
    assert a.value == 5
    a.mult(3)
    assert a.value == 15


def test_cell_integer_multiplication():
    a = Cell(5)
    assert a.value == 5
    a.mult(3)
    assert a.value == 15


def test_cell_distributive_property():
    a = Cell()
    a.add(3)
    a.add(4)
    a.mult(2)
    assert a.value == 14


def test_sequence_and_timing():
    a = Cell(5, name="a")
    previous = a
    cells = []
    for _ in range(100):
        cell = Cell(previous)
        cells.append(cell)
        previous = cell
    a.value = 99
    assert cells[-1].value == 99


def test_cell_rounding():
    a = Cell(1.234567)
    assert round(a, 2) == 1.23
    assert round(a, 3) == 1.235


def test_formula_updates():
    a = Cell(5, "a")
    b = Cell(3, "b")
    c = 4 * (a + b) / 2
    b.value = 4
    assert c.value == 18

# TODO: test decimal math


# def test_constant():
#     a = Constant(9)
#     a.value = 10
#     assert a.value == 9
