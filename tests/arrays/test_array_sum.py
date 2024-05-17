from sheetcake import Array, ArraySum
import pytest


def test_adding_one_array_to_array_sum():
    c = ArraySum(arrays=[], name='c', duration=3)
    a = Array.from_values(values=(-10, 20, 30), name='a')
    c.add_item(a)
    assert c.get_value(0) == -10
    assert c.get_value(1) == 20
    assert c.get_value(2) == 30
    assert c.total == 40


def test_adding_two_arrays_to_array_sum():
    c = ArraySum(arrays=[], name='c', duration=3)
    a = Array.from_values(values=(10, 20, 30), name='a')
    b = Array.from_values(values=(40, 50, 60), name='b')
    c.add_item(a)
    c.add_item(b)
    assert c.get_value(0) == 50
    assert c.get_value(1) == 70
    assert c.get_value(2) == 90
    assert c.total == 210


def test_adding_nested_array_sum_updating():
    a = Array.from_values(values=(1, 2, 3), name='a')
    b = Array.from_values(values=(10, 20, 30), name='b')
    c = ArraySum(arrays=[a, b], name='c', duration=3)
    d = Array.from_values(values=(100, 200, 300), name='d')
    e = ArraySum(arrays=[c, d], name='e', duration=3)
    a.set_value(0, 0)
    a.set_value(1, 0)
    a.set_value(2, 0)
    assert e[0] == 110
    assert e[1] == 220
    assert e[2] == 330
    assert e.total == 660


def test_array_sum_no_duration_raises_error():
    with pytest.raises(Exception):
        c = ArraySum(arrays=[], name='c')


def test_array_sum_different_duration_raises_error():
    a = Array.from_values(values=(1, 2, 3), name='a')
    b = Array.from_values(values=(10, 20, 30, 40), name='b')
    with pytest.raises(Exception):
        c = ArraySum(arrays=[a, b], name='c')


def test_array_sum_add_wrong_duration_raises_error():
    a = Array.from_values(values=(1, 2, 3), name='a')
    b = Array.from_values(values=(10, 20, 30), name='b')
    c = ArraySum(arrays=[a, b], name='c', duration=3)
    d = Array.from_values(values=(100, 200, 300, 400), name='d')
    with pytest.raises(Exception):
        c.add_item(d)


def test_array_sum_repr():
    a = Array.from_values(values=(1, 2, 3), name='a')
    b = Array.from_values(values=(10, 20, 30), name='b')
    c = ArraySum(arrays=[a, b], name='c', duration=3)
    repr(c)
    assert True
