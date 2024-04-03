from sheetcake import Cell


def test_cell_integer_multiplication():
    a = Cell()
    a.equal(5)
    assert a.value == 5
    a.mult(3)
    assert a.value == 15


def test_cell_multiplication():
    a = Cell(3)
    b = Cell(4)
    c = Cell()
    c.mult(a)
    c.mult(b)
    assert c.value == 12


def test_cell_distributive_property():
    a = Cell()
    a.add(3)
    a.add(4)
    a.mult(2)
    assert a.value == 14


def test_cell_multiplication_operator():
    a = Cell(5)
    b = Cell(3)
    c = a * b
    assert c.value == 15


def test_multiplication_int_one_by_zero_cell():
    a = Cell(0)
    b = 1 * a
    assert b.value == 0


def test_multiplication_zero_cell_by_int_one():
    a = Cell(0)
    b = a * 1
    assert b.value == 0


def test_cell_multiplication_updates():
    a = Cell(10)
    b = Cell(4)
    c = a * b
    b.value = 5
    assert c.value == 50


def test_multiplication_int_cell():
    a = 5
    b = Cell(3)
    c = a * b
    assert c.value == 15


def test_multiplication_cell_int():
    a = 5
    b = Cell(3)
    c = b * a
    assert c.value == 15


def test_negative_cell():
    a = Cell(5)
    b = -a
    assert b.value == -5


def test_negative_cell_updates():
    a = Cell(5)
    b = -a
    a.value = 99
    assert b.value == -99
