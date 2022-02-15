from sheetcake import Array
from sheetcake import Cell
from sheetcake.src.arrays.array import zeros
import pytest


@pytest.fixture
def array_a():
    return Array(array=(10, 20, 30), name='a')


@pytest.fixture
def array_b():
    return Array(array=(40, 50, 60), name='b')


@pytest.fixture
def array_hundreds():
    return Array(array=(-100, 0, 100), name='hundreds')


def test_subtracting_two_arrays(array_a, array_b):
    c = array_b - array_a
    assert c[0].value == 30
    assert c[1].value == 30
    assert c[2].value == 30
    assert c.total == 90


def test_subtracting_cell_from_array(array_a):
    b = Cell(4, name='b')
    c = array_a - b
    assert c[0] == 6
    assert c[1] == 16
    assert c[2] == 26
    assert c.total == 48


def test_subtracting_array_from_cell(array_a):
    b = Cell(100, name='b')
    c = b - array_a
    assert c[0] == 90
    assert c[1] == 80
    assert c[2] == 70
    assert c.total == 240


def test_subtracting_int_from_array(array_a):
    c = array_a - 4
    assert c[0] == 6
    assert c[1] == 16
    assert c[2] == 26
    assert c.total == 48


def test_subtracting_array_from_int(array_a):
    c = 40 - array_a
    assert c[0] == 30
    assert c[1] == 20
    assert c[2] == 10
    assert c.total == 60


def test_array_subtraction_updating_value_updates_result(array_a, array_b):
    c = array_b - array_a
    array_a.set_value(0, 100)
    array_b.set_value(0, 400)
    assert c[0] == 300
    assert c[1] == 30
    assert c[2] == 30
    assert c.total == 360


def test_scalar_subtraction_updating_value_cascades_all_results(array_a, array_b):
    c = Array(array=(70, 80, 90), name='d')
    d = array_b - array_a
    e = d - c
    array_a.set_value(0, 1)
    assert d[0] == 39
    assert e[0] == -31
    assert e.total == -141


def test_subtracting_array_from_cell_updates(array_hundreds):
    b = Cell(40, name='b')
    c = b - array_hundreds
    b.value = 400
    assert c[0] == 500
    assert c[1] == 400
    assert c[2] == 300
    assert c.total == 1200


def test_array_subtraction_updating_array_updates_result(array_a, array_b):
    c = array_b - array_a
    array_b.set_values((100, 200, 300))
    assert c[0] == 90
    assert c[1] == 180
    assert c[2] == 270


def test_subtracting_multiple_arrays():
    a = Array(array=(1, 2, 3), name='a')
    b = Array(array=(10, 20, 30), name='b')
    c = Array(array=(111, 222, 333), name='c')
    d = c - a - b
    assert d[0] == 100
    assert d[1] == 200
    assert d[2] == 300


def test_subtracting_multiple_arrays_updating():
    a = Array(array=(1, 2, 3), name='a')
    b = Array(array=(10, 20, 30), name='b')
    c = Array(array=(111, 222, 333), name='c')
    d = c - a - b
    a.set_values((0, 0, 0))
    assert d[0] == 101
    assert d[1] == 202
    assert d[2] == 303


def test_subtracting_nested_arrays_updating():
    a = Array(array=(1, 2, 3), name='a')
    b = Array(array=(10, 20, 30), name='b')
    c = Array(array=(111, 222, 333), name='c')
    d = c - b
    e = d - a
    a.set_values((0, 0, 0))
    assert e[0] == 101
    assert e[1] == 202
    assert e[2] == 303
    assert e.total == 606


def test_subtracting_nested_arrays_and_scalars_updating():
    a = Cell(100)
    b = Array(array=(10, 20, -1), name='b')
    c = Array(array=(100, 200, 0), name='c')
    d = a - b
    e = d - c
    a.value = 0
    assert e[0] == -110
    assert e[1] == -220
    assert e[2] == 1
