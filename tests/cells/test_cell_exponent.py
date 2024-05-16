from sheetcake import Cell


def test_cell_integer_exp():
    a = Cell()
    a.equal_cell(2)
    assert a.value == 2
    a.exp_cell(3)
    assert a.value == 8


def test_cell_exp():
    a = Cell(2)
    b = Cell(3)
    a.exp_cell(b)
    assert a.value == 8


def test_cell_exp_operator():
    a = Cell(2)
    b = Cell(3)
    c = a ** b
    assert c.value == 8


def test_cell_exp_add():
    a = Cell(2)
    a.exp_cell(2)
    a.add_cell(1)
    assert a.value == 5


def test_cell_exp_expression():
    a = Cell(2)
    b = Cell(2)
    a.exp_cell(b + 1)
    assert a.value == 8


def test_cell_exp_updates():
    a = Cell(10)
    b = Cell(2)
    c = a ** b
    assert c.value == 100
    b.value = 3
    assert c.value == 1000


def test_cell_exp_none():
    a = Cell()
    a.exp_cell(2)
    assert a.value == 2
