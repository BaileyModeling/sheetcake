from sheetcake import Array, Cell
import pytest


def test_multiplying_two_arrays():
    a = Array.from_values(values=(-1, 2, 5), name='a')
    b = Array.from_values(values=(6, 7, 0), name='b')
    c = a * b
    assert c[0] == -6
    assert c[1] == 14
    assert c[2] == 0
    assert c.total == 8


def test_multiplying_two_arrays_diff_len_raises_error():
    a = Array.from_values(values=(-1, 2, 5), name='a')
    b = Array.from_values(values=(6, 7, 0, 1, 1, 1), name='b')
    with pytest.raises(Exception):
        c = a * b


def test_multiplying_array_and_str_raises_error():
    a = Array.from_values(values=(3., 4., 5.5), name='a')
    b = "string"
    with pytest.raises(Exception):
        c = a * b


def test_multiplying_array_and_cell():
    a = Array.from_values(values=(3., 4., 5.5), name='a')
    b = Cell(10, name='b')
    c = a * b
    assert c[0] == 30
    assert c[1] == 40
    assert c[2] == 55


def test_multiplying_array_and_cell_method():
    a = Array.from_values(values=(3., 4., 5.5), name='a')
    b = Cell(10, name='b')
    c = a.mult(b)
    assert c[0] == 30
    assert c[1] == 40
    assert c[2] == 55


def test_multiplying_array_and_string_method():
    a = Array.from_values(values=(3., 4., 5.5), name='a')
    with pytest.raises(Exception):
        c = a.mult("string")


def test_multiplying_cell_and_array():
    a = Array.from_values(values=(3., 4., 5.5), name='a')
    b = Cell(10, name='b')
    c = b * a
    assert c[0] == 30
    assert c[1] == 40
    assert c[2] == 55


def test_multiplying_array_and_int():
    a = Array.from_values(values=(3., 4., 5.5), name='a')
    b = 10
    c = a * b
    assert c[0] == 30
    assert c[1] == 40
    assert c[2] == 55


def test_multiplying_int_and_array():
    a = Array.from_values(values=(3., 0.0, 5.5), name='a')
    b = 10
    c = b * a
    assert c[0] == 30
    assert c[1] == 0
    assert c[2] == 55


def test_array_multiplication_updating_value_updates_result():
    a = Array.from_values(values=(1., 2., 3.), name='a')
    b = Array.from_values(values=(4., 5., 6.), name='b')
    c = a * b
    a.set_value(0, 0)
    b.set_value(1, 50)
    assert c[0] == 0
    assert c[1] == 100
    assert c[2] == 18


def test_array_multiplication_updating_slice_updates_result():
    a = Array.from_values(values=(1., 2., 3.), name='a')
    b = Array.from_values(values=(4., 5., 6.), name='b')
    c = a * b
    a.set_values([100, 100, 100])
    assert c[0] == 400.
    assert c[1] == 500.
    assert c[2] == 600.
    assert c.total == 1500.


def test_cell_multiplication_updating_value_cascades_all_results():
    a = Array.from_values(values=(1., 2., 3.), name='a')
    b = Array.from_values(values=(4., 5., 6.), name='b')
    c = a * b
    d = Cell(10, name='d')
    e = d * c
    a.set_value(0, 9)
    assert e[0] == 360
    assert e[1] == 100
    assert e[2] == 180
    assert e.total == 640
