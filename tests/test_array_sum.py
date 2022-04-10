from sheetcake.src.arrays.array_sum import ArraySum
from sheetcake import Array


def test_adding_one_array_to_array_sum():
    c = ArraySum(name='c', duration=3)
    a = Array(array=(-10, 20, 30), name='a')
    c.add(a)
    assert c.get_value(0) == -10
    assert c.get_value(1) == 20
    assert c.get_value(2) == 30


def test_adding_two_arrays_to_array_sum():
    c = ArraySum(name='c', duration=3)
    a = Array(array=(10, 20, 30), name='a')
    b = Array(array=(40, 50, 60), name='b')
    c.add(a)
    c.add(b)
    assert c.get_value(0) == 50
    assert c.get_value(1) == 70
    assert c.get_value(2) == 90


def test_adding_nested_array_sum_updating():
    a = Array(array=(1, 2, 3), name='a')
    b = Array(array=(10, 20, 30), name='b')
    c = Array(array=(100, 200, 300), name='c')
    d = ArraySum(a, b, name='d')
    e = ArraySum(d, c, name='e')
    a.set_value(0, 0)
    a.set_value(1, 0)
    a.set_value(2, 0)
    assert e[0] == 110
    assert e[1] == 220
    assert e[2] == 330
    assert e.total == 660
