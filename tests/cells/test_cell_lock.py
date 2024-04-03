from sheetcake2 import Cell


def test_cell_lock():
    a = Cell(5)
    a.lock()
    a.value = 100
    assert a.value == 5


def test_cell_unlock():
    a = Cell(5)
    a.lock()
    a.value = 100
    a.unlock()
    a.value = 50
    assert a.value == 50


def test_cell_lock_with_formula():
    a = Cell(5)
    b = Cell()
    b.equal(a)
    assert b.value == 5
    b.lock()
    a.value = 100
    assert b.value == 5


def test_cell_lock_value():
    a = Cell()
    a.lock_value(5)
    a.value = 100
    assert a.value == 5
