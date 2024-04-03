from datetime import date
from sheetcake import dates


def test_next_month():
    end = dates.next_month(date(2022, 1, 15))
    assert end == date(2022, 2, 1)


def test_next_month_beginning_of_month():
    end = dates.next_month(date(2022, 1, 1))
    assert end == date(2022, 2, 1)


def test_next_month_february():
    end = dates.next_month(date(2022, 2, 28))
    assert end == date(2022, 3, 1)


def test_next_month_none():
    end = dates.next_month(None)
    result = date.today()
    assert end == dates.beginning_of_month(dates.edate(result, 1))
