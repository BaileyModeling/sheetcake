from sheetcake import Array, Cell
import pytest


def test_array_length():
    a = Array.blank(5)
    assert len(a) == 5


def test_array_init():
    a = Array.from_values(values=[1, 2, 3, 4, 5])
    assert a[0].value == 1


def test_array_init_total():
    a = Array.from_values(values=[1, 2, 3, 4, 5])
    assert a.total.value == 15


def test_array_total_updates():
    a = Array.from_values(values=[1, 2, 3, 4, 5])
    a.set_value(4, 0)
    assert a.total == 10


def test_set_values_method():
    a = Array.zeros(10)
    a.set_values([1]*4, start=6)
    assert a.get_value(0) == 0
    assert a.get_value(6) == 1
    assert a.get_value(9) == 1


def test_array_init_values():
    a = Array.from_values(values=[0, 1, 2, 3])
    assert a.get_value(0) == 0
    assert a.get_value(1) == 1
    assert a.total == 6


def test_zeros():
    a = Array.zeros(10)
    assert a.get_value(0) == 0
    assert a.total == 0


def test_array_equal_method_string():
    a = Array.from_values(values=(10, 20, 30), name='a')
    with pytest.raises(Exception):
        c = a.equal("string")


# initialize array with list of existing Cells
# make sure it's the same object
def test_array_initialized_with_existing_cells():
    a = Cell(0, "a")
    b = Cell(1, "b")
    array = Array(array=[a, b])
    assert array[0] is a
    assert array[1] is b


def test_array_print():
    a = Array.from_values(values=(10, 20, 30), name='a')
    a.print()
    assert True


def test_array_print_cells():
    a = Array.from_values(values=(10, 20, 30), name='a')
    a.print_cells()
    assert True


def test_array_print_row():
    a = Array.from_values(values=(10, 20, 30), name='a')
    a.print_row()
    assert True


def test_array_print_formulas():
    a = Array.from_values(values=(10, 20, 30), name='a')
    a.print_formulas()
    assert True


def test_array_print_value_audit():
    a = Array.from_values(values=(10, 20, 30), name='a')
    a.print_value_audit()
    assert True


def test_array_str():
    a = Array.from_values(values=(10, 20, 30), name='a')
    print(str(a))
    assert True


def test_array_total_updates_after_append():
    a = Array.from_values(values=(10, 20, 30), name='a')
    a.append(Cell(40))
    assert a.total == 100
