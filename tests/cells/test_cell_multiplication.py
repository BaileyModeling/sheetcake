from sheetcake import Cell


def test_cell_integer_multiplication():
    a = Cell()
    a.equal_item(5)
    assert a.value == 5
    a.mult_item(3)
    assert a.value == 15


def test_cell_multiplication():
    a = Cell(3)
    b = Cell(4)
    c = Cell()
    c.mult_item(a)
    c.mult_item(b)
    assert c.value == 12


def test_cell_distributive_property():
    a = Cell()
    a.add_item(3)
    a.add_item(4)
    a.mult_item(2)
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


def test_mult_cell_class_method():
    a = Cell(2)
    b = Cell(5)
    c = Cell(6)
    d = Cell.mult([a, b, c], name="mult_cell")
    assert d.value == 60
    a.value = 20
    assert d.value == 600
