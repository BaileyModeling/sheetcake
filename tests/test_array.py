from sheetcake import Array
from sheetcake import Cell
from sheetcake.src.arrays.array import zeros


def test_array_length():
    a = Array(5)
    assert len(a) == 5


def test_array_init_total():
    a = Array(array=[1, 2, 3, 4, 5])
    assert a.total == 15


def test_array_total_updates():
    a = Array(array=[1, 2, 3, 4, 5])
    a.set_value(4, 0)
    assert a.total == 10


def test_set_values_method():
    a = zeros(10)
    a.set_values([1]*4, start=6)
    assert a.get_value(6) == 1
    assert a.total == 4


def test_array_init_values():
    a = Array(array=[0, 1, 2, 3])
    assert a.get_value(0) == 0
    assert a.get_value(1) == 1
    assert a.total == 6


def test_zeros():
    a = zeros(10)
    assert a.get_value(0) == 0
    assert a.total == 0


# initialize array with list of existing Cells
# make sure it's the same object
def test_array_initialized_with_existing_cells():
    a = Cell(0, "a")
    b = Cell(1, "b")
    array = Array(array=[a, b])
    assert array[0] is a
    assert array[1] is b
