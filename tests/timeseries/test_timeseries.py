from sheetcake import TimeSeries, DateArray
from datetime import date
import pytest


def test_timeseries_repr():
    da = DateArray(date(2024, 1, 1), 3)
    a = TimeSeries.from_values(date_array=da, values=(10, 20, 30), name='a')
    repr(a)
    assert True


def test_timeseries_print():
    da = DateArray(date(2024, 1, 1), 3)
    a = TimeSeries.from_values(date_array=da, values=(10, 20, 30), name='a')
    a.print()
    assert True


def test_timeseries_datearray_array_length_mismatch():
    da = DateArray(date(2024, 1, 1), 12)
    with pytest.raises(ValueError):
        TimeSeries.from_values(date_array=da, values=(10, 20, 30), name='a')