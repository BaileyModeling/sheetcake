from sheetcake import Array, Cell, TimeSeries, DateArray
from types import SimpleNamespace
from datetime import date
import pytest


@pytest.fixture
def tsa() -> TimeSeries:
    da = DateArray(date(2024, 1, 1), 3)
    return TimeSeries.from_values(date_array=da, values=(10, 20, 30), name='a')


def test_adding_two_timeseries():
    da = DateArray(date(2024, 1, 1), 3)
    a = TimeSeries.from_values(date_array=da, values=(10, 20, 30), name='a')
    b = TimeSeries.from_values(date_array=da, values=(40, 50, 60), name='b')
    c = a + b
    assert c.get_value(0) == 50
    assert c.get_value(1) == 70
    assert c.get_value(2) == 90
    assert c.total == 210


def test_adding_two_timeseries_with_add_method():
    da = DateArray(date(2024, 1, 1), 3)
    a = TimeSeries.from_values(date_array=da, values=(10, 20, 30), name='a')
    b = TimeSeries.from_values(date_array=da, values=(40, 50, 60), name='b')
    a.add(b)
    assert a.get_value(0) == 50
    assert a.get_value(1) == 70
    assert a.get_value(2) == 90
    assert a.total == 210


def test_adding_timeseries_and_cell(tsa: TimeSeries):
    b = Cell(40, name='b')
    c = tsa + b
    assert c[0] == 50
    assert c[1] == 60
    assert c[2] == 70


def test_adding_cell_and_timeseries(tsa: TimeSeries):
    b = Cell(40, name='b')
    c = b + tsa
    assert c[0] == 50
    assert c[1] == 60
    assert c[2] == 70


def test_adding_timeseries_add_method_cell(tsa: TimeSeries):
    b = Cell(40, name='b')
    c = tsa.add(b)
    assert c[0] == 50
    assert c[1] == 60
    assert c[2] == 70


def test_adding_timeseries_add_method_string_raises_error():
    da = DateArray(date(2024, 1, 1), 3)
    a = TimeSeries.from_values(date_array=da, values=(10, 20, 30), name='a')
    with pytest.raises(Exception):
        c = a.add("string")


def test_adding_timeseries_add_string_raises_error(tsa: TimeSeries):
    with pytest.raises(Exception):
        c = tsa + "string"


def test_adding_timeseries_and_int(tsa: TimeSeries):
    b = 40
    c = tsa + b
    assert c[0] == 50
    assert c[1] == 60
    assert c[2] == 70


def test_adding_timeseries_and_int_updates(tsa: TimeSeries):
    b = 40
    c = tsa + b
    tsa.set_value(2, 40)
    assert c[0] == 50
    assert c[1] == 60
    assert c[2] == 80
    assert c.total == 190


def test_adding_multiple_timeseries_updating():
    da = DateArray(date(2024, 1, 1), 3)
    a = TimeSeries.from_values(date_array=da, values=(1, 2, 3), name='a')
    b = TimeSeries.from_values(date_array=da, values=(10, 20, 30), name='b')
    c = TimeSeries.from_values(date_array=da, values=(100, 200, 300), name='c')
    d = sum((a, b, c))
    a.set_value(0, 0)
    a.set_value(1, 0)
    a.set_value(2, 0)
    assert d[0] == 110
    assert d[1] == 220
    assert d[2] == 330
    assert d.total == 660


def test_adding_two_timeseries_unequal_len_raises_error():
    a = TimeSeries.from_values(date_array=DateArray(date(2024, 1, 1), 3), values=(1, 2, 3), name='a')
    b = TimeSeries.from_values(date_array=DateArray(date(2024, 1, 1), 4), values=(10, 20, 30, 40), name='b')
    with pytest.raises(Exception):
        c = a + b


def test_adding_two_timeseries_unequal_date_array_raises_error():
    a = TimeSeries.from_values(date_array=DateArray(date(2024, 1, 1), 3), values=(1, 2, 3), name='a')
    b = TimeSeries.from_values(date_array=DateArray(date(2025, 1, 1), 3), values=(10, 20, 30), name='b')
    with pytest.raises(Exception):
        c = a + b


def test_adding_timeseries_simplenamespace_raises_error(tsa: TimeSeries):
    b = SimpleNamespace(value=40, name='b')
    with pytest.raises(Exception):
        c = tsa + b


def test_timeseries_zeros():
    da = DateArray(date(2024, 1, 1), 3)
    a = TimeSeries.zeros(date_array=da, name='a')
    assert a[0] == 0
    assert a[1] == 0
    assert a[2] == 0
    assert a.total == 0
