from sheetcake import Array, Cell
from sheetcake.src.arrays.array import is_scalar
from types import SimpleNamespace
import numpy as np
import pytest


def test_array_subtraction():
    a = Array.from_values(values=(-100, 0, 100), name='a')
    b = Array.from_values(values=(100, 100, -200), name='b')
    c = a - b
    assert c[0].value == -200
    assert c[1].value == -100
    assert c[2].value == 300


def test_list_array_subtraction():
    a = [-100, 0, 100]
    b = Array.from_values(values=(100, 100, -200), name='b')
    c = a - b
    assert c[0].value == -200
    assert c[1].value == -100
    assert c[2].value == 300


def test_list_array_subtraction_unequal_len_raises_error():
    a = [-100, 0, 100, 1, 1, 1]
    b = Array.from_values(values=(100, 100, -200), name='b')
    with pytest.raises(Exception):
        c = a - b


def test_array_subtraction_unequal_len_raises_error():
    a = Array.from_values(values=(-100, 0, 100, 200, 300), name='a')
    b = Array.from_values(values=(100, 100, -200), name='b')
    with pytest.raises(Exception):
        c = a - b


def test_array_subtraction_string_raises_error():
    a = Array.from_values(values=(-100, 0, 100), name='a')
    b = "string"
    with pytest.raises(Exception):
        c = a - b


def test_array_int_subtraction():
    a = Array.from_values(values=(-100, 0, 100), name='a')
    b = 10
    c = a - b
    assert c[0].value == -110
    assert c[1].value == -10
    assert c[2].value == 90


def test_int_array_subtraction():
    a = Array.from_values(values=(-100, 0, 100), name='a')
    b = 10
    c = b - a
    assert c[0].value == 110
    assert c[1].value == 10
    assert c[2].value == -90


def test_array_cell_subtraction():
    a = Array.from_values(values=(-100, 0, 100), name='a')
    b = Cell(10, "b")
    c = a - b
    assert c[0].value == -110
    assert c[1].value == -10
    assert c[2].value == 90


def test_cell_array_subtraction():
    a = Array.from_values(values=(-100, 0, 100), name='a')
    b = Cell(10, "b")
    c = b - a
    assert c[0].value == 110
    assert c[1].value == 10
    assert c[2].value == -90


def test_array_string_subtraction_raises_error():
    a = Array.from_values(values=(-100, 0, 100), name='a')
    b = "string"
    with pytest.raises(Exception):
        c = b - a


def test_is_scalar_numpy_element():
    a = np.array([1, 2, 3])
    assert is_scalar(a[0])


def test_is_scalar_numpy_array():
    a = np.array([1, 2, 3])
    assert not is_scalar(a)


def test_sub_operator_array_simplenamespaces_raises_error():
    a = Array.from_values(values=(10, 20, 30), name='a')
    b = SimpleNamespace(value=40, name='b')
    with pytest.raises(Exception):
        a - b


def test_rsub_operator_array_simplenamespaces_raises_error():
    a = Array.from_values(values=(10, 20, 30), name='a')
    b = SimpleNamespace(value=40, name='b')
    with pytest.raises(Exception):
        b - a
