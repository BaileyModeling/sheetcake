from sheetcake import Array, Cell
from sheetcake.src.arrays.array import zeros
import pytest


def test_dividing_two_arrays():
    a = Array(array=(4, 9, 16), name='a')
    b = Array(array=(2, 3, 4), name='b')
    c = a / b
    assert c[0] == 2
    assert c[1] == 3
    assert c[2] == 4


def test_dividing_array_by_cell():
    a = Array(array=(30., 40., 5.5), name='a')
    b = Cell(10, name='b')
    c = a / b
    assert c[0] == 3
    assert c[1] == 4
    assert c[2] == 0.55


def test_dividing_cell_by_array():
    a = Array(array=(2, 3, 4), name='a')
    b = Cell(60, name='b')
    c = b / a
    assert c[0] == 30
    assert c[1] == 20
    assert c[2] == 15


def test_dividing_int_by_array():
    a = Array(array=(2, 3, 4), name='a')
    b = 60
    c = b / a
    assert c[0] == 30
    assert c[1] == 20
    assert c[2] == 15


def test_array_division_updating_value_updates_result():
    a = Array(array=(60., 180., 360.), name='a')
    b = Array(array=(2., 4., 6.), name='b')
    c = a / b
    b.set_value(0, 10)
    b.set_value(1, 90)
    assert c[0] == 6
    assert c[1] == 2
    assert c[2] == 60


def test_array_division_updating_slice_updates_result():
    a = Array(array=(100., 200., 300.), name='a')
    b = Array(array=(10., 20., 30.), name='b')
    c = a / b
    a.set_values([1000, 2000, 3000])
    assert c[0] == 100
    assert c[1] == 100
    assert c[2] == 100
    assert c.total == 300


def test_cell_division_updating_value_cascades_all_results():
    a = Array(array=(60., 180., 360.), name='a')
    b = Array(array=(2., 4., 6.), name='b')
    c = a / b
    d = Cell(60, name='d')
    e = d / c
    a.set_value(0, 50)
    b.set_value(0, 10)
    b.set_value(1, 90)
    assert e[0] == 12
    assert e[1] == 30
    assert e[2] == 1
    assert e.total == 43
