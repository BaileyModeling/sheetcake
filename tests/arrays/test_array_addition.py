from sheetcake import Array, Cell
from decimal import Decimal
import pytest


def test_adding_two_arrays():
    a = Array.from_values(values=(10, 20, 30), name='a')
    b = Array.from_values(values=(40, 50, 60), name='b')
    c = a + b
    assert c.get_value(0) == 50
    assert c.get_value(1) == 70
    assert c.get_value(2) == 90
    assert c.total == 210


def test_adding_two_arrays_with_add_method():
    a = Array.from_values(values=(10, 20, 30), name='a')
    b = Array.from_values(values=(40, 50, 60), name='b')
    a.add(b)
    assert a.get_value(0) == 50
    assert a.get_value(1) == 70
    assert a.get_value(2) == 90
    assert a.total == 210


def test_adding_array_and_cell():
    a = Array.from_values(values=(10, 20, 30), name='a')
    b = Cell(40, name='b')
    c = a + b
    assert c[0] == 50
    assert c[1] == 60
    assert c[2] == 70


def test_adding_cell_and_array():
    a = Array.from_values(values=(10, 20, 30), name='a')
    b = Cell(40, name='b')
    c = b + a
    assert c[0] == 50
    assert c[1] == 60
    assert c[2] == 70


def test_adding_array_add_method():
    a = Array.from_values(values=(10, 20, 30), name='a')
    b = Cell(40, name='b')
    c = a.add(b)
    assert c[0] == 50
    assert c[1] == 60
    assert c[2] == 70


def test_adding_array_add_method_string_raises_error():
    a = Array.from_values(values=(10, 20, 30), name='a')
    with pytest.raises(Exception):
        c = a.add("string")


def test_adding_array_add_string_raises_error():
    a = Array.from_values(values=(10, 20, 30), name='a')
    with pytest.raises(Exception):
        c = a + "string"


def test_adding_array_and_int():
    a = Array.from_values(values=(10, 20, 30), name='a')
    b = 40
    c = a + b
    assert c[0] == 50
    assert c[1] == 60
    assert c[2] == 70


def test_adding_array_and_int_updates():
    a = Array.from_values(values=(10, 20, 30), name='a')
    b = 40
    c = a + b
    a.set_value(2, 40)
    assert c[0] == 50
    assert c[1] == 60
    assert c[2] == 80
    assert c.total == 190


def test_adding_multiple_arrays_updating():
    a = Array.from_values(values=(1, 2, 3), name='a')
    b = Array.from_values(values=(10, 20, 30), name='b')
    c = Array.from_values(values=(100, 200, 300), name='c')
    d = sum((a, b, c))
    a.set_value(0, 0)
    a.set_value(1, 0)
    a.set_value(2, 0)
    assert d[0] == 110
    assert d[1] == 220
    assert d[2] == 330
    assert d.total == 660


def test_adding_nested_arrays_updating():
    a = Array.from_values(values=(1, 2, 3), name='a')
    b = Array.from_values(values=(10, 20, 30), name='b')
    c = Array.from_values(values=(100, 200, 300), name='c')
    d = a + b
    e = d + c
    a.set_value(0, 0)
    a.set_value(1, 0)
    a.set_value(2, 0)
    assert e[0] == 110
    assert e[1] == 220
    assert e[2] == 330
    assert e.total == 660


def test_adding_array_and_decimal():
    a = Array.zeros(10)
    b = Decimal(2.3)
    c = a + b
    assert round(float(c.get_value(0)), 4) == 2.3
    assert int(round(c.total, 4)) == 23


def test_adding_two_arrays_unequal_len_raises_error():
    a = Array.from_values(values=(10, 20, 30), name='a')
    b = Array.from_values(values=(40, 50, 60, 70, 80), name='b')
    with pytest.raises(Exception):
        c = a + b
