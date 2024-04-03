from datetime import date
import pytest
from sheetcake import DateArray
from types import SimpleNamespace


def test_date_array_debug_dict():
    obj = DateArray(date(2022,1,1), 12)
    assert isinstance(obj.debug_dict, dict)


def test_date_array_index_ym():
    obj = DateArray(date(2022,1,1), 12)
    assert 0 == obj.index_ym(2022, 1)
    assert 1 == obj.index_ym(2022, 2)


def test_date_array_end_date():
    obj = DateArray(date(2022,1,1), 12)
    assert date(2022, 12,31) == obj.end_date


def test_date_array_index():
    obj = DateArray(date(2022,1,1), 12)
    assert 0 == obj.index(date(2022, 1, 31))
    assert 1 == obj.index(date(2022, 2, 15))


def test_date_array_days_array():
    da = DateArray(date(2022,1,1), 12)
    obj = da.days
    assert 31 == obj[0].value
    assert 28 == obj[1].value


def test_date_array_year_index():
    da = DateArray(date(2020,7,1), 12)
    start, end = da.year_index(2020)
    assert start == 0
    assert end == 5


def test_date_array_year_index2():
    da = DateArray(date(2020,7,1), 12)
    start, end = da.year_index(2021)
    assert start == 6
    assert end == 11


def test_date_array_year_index_inclusive():
    da = DateArray(date(2020,7,1), 12)
    start, end = da.year_index(2020, inclusive=True)
    assert start == 0
    assert end == 6


def test_date_array_year_index2_inclusive():
    da = DateArray(date(2020,7,1), 12)
    start, end = da.year_index(2021, inclusive=True)
    assert start == 6
    assert end == 12


def test_date_array_year_index_earlier_year():
    da = DateArray(date(2020,7,1), 12)
    start, end = da.year_index(2010)
    assert start is None
    assert end is None


def test_date_array_years():
    da = DateArray(date(2020,12,1), 14)
    assert len(da.years) == 3
    assert da.years[0] == 2020
    assert da.years[1] == 2021
    assert da.years[2] == 2022


def test_date_array_years_single():
    da = DateArray(date(2020,7,1), 1)
    assert len(da.years) == 1
    assert da.years[0] == 2020


def test_date_array_zero_duration_raises_error():
    with pytest.raises(ValueError):
        da = DateArray(date(2020,7,1), 0)


def test_date_array_equal_date_array():
    da1 = DateArray(date(2024,1,1), 12)
    da2 = DateArray(date(2024,1,1), 12)
    assert da1 == da2


def test_date_array_not_equal_date_array_start():
    da1 = DateArray(date(2024,1,1), 12)
    da2 = DateArray(date(2025,1,1), 12)
    assert not da1 == da2


def test_date_array_not_equal_date_array_duration():
    da1 = DateArray(date(2024,1,1), 12)
    da2 = SimpleNamespace(start_date = date(2024,1,1))
    assert not da1 == da2


def test_date_array_not_equal_none():
    da1 = DateArray(date(2024,1,1), 12)
    da2 = None
    assert not da1 == da2


def test_date_array_prorated_days():
    da = DateArray(date(2023,1,1), 12)
    days = da.prorated_days(date(2023,2,15))
    assert days[0] == 31
    assert days[1] == 14
    assert days[2] == 0
