from datetime import date
from sheetcake import dates


def test_eomonth_range():
    rng = list(dates.eomonth_range(date(2022, 1, 31), 3))
    assert rng[0] == date(2022, 1, 31)
    assert rng[1] == date(2022, 2, 28)
    assert rng[2] == date(2022, 3, 31)
    assert len(rng) == 3


def test_eomonth_range_start_is_not_eomonth():
    rng = list(dates.eomonth_range(date(2022, 1, 1), 3))
    assert rng[0] == date(2022, 1, 31)
    assert rng[1] == date(2022, 2, 28)
    assert rng[2] == date(2022, 3, 31)
    assert len(rng) == 3


def test_eomonth_range_zero_duration():
    rng = list(dates.eomonth_range(date(2022, 1, 31), 0))
    assert len(rng) == 0


def test_eomonth_range_negative_duration():
    rng = list(dates.eomonth_range(date(2022, 1, 31), -3))
    assert len(rng) == 0
