from sheetcake import Cell


def test_blank_cell_integer_subtraction():
    a = Cell()
    a.sub_cell(5)
    assert a.value == -5
    a.sub_cell(3)
    assert a.value == -8


def test_cell_integer_subtraction():
    a = Cell()
    a.equal_cell(8)
    a.sub_cell(3)
    assert a.value == 5


def test_cell_subtraction():
    a = Cell(8)
    b = Cell(3)
    c = Cell()
    c.add_cell(a)
    c.sub_cell(b)
    assert c.value == 5


def test_cell_subtraction_updates():
    a = Cell(10)
    b = Cell(3)
    c = Cell()
    c.add_cell(a)
    c.sub_cell(b)
    a.value = 8
    assert c.value == 5


def test_cell_subtraction_operator():
    a = Cell(8)
    b = Cell(3)
    c = a - b
    assert c.value == 5


def test_integer_minus_cell():
    a = Cell(8)
    b = 5 - a
    assert b.value == -3


def test_cell_subtraction_by_zero():
    a = Cell(10)
    b = Cell(0)
    c = a - b
    assert c.value == 10
