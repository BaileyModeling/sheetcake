from datetime import date
from sheetcake import dates


def test_edate():
    end = dates.edate(date(2022, 1, 15), 12)
    assert end == date(2023, 1, 15)


def test_edate_beginning_of_month():
    end = dates.edate(date(2022, 1, 1), 1)
    assert end == date(2022, 2, 1)


def test_edate_0():
    end = dates.edate(date(2022, 1, 15), 0)
    assert end == date(2022, 1, 15)


def test_edate_negative():
    end = dates.edate(date(2022, 1, 15), -1)
    assert end == date(2021, 12, 15)


def test_edate_february():
    result = dates.edate(date(2022,1,31), 1)
    assert result == date(2022, 2, 28)


def test_edate_not_inclusive():
    end = dates.edate(date(2022, 1, 15), 12, inclusive=False)
    assert end == date(2023, 1, 14)
