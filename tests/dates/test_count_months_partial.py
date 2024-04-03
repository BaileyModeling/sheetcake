from datetime import date, timedelta
from sheetcake import dates


def test_count_months_partial():
    result = dates.count_months_partial(date(2022,2,15), date(2022, 2, 28))
    assert result == 0.5


def test_count_months_partial_whole_months():
    result = dates.count_months_partial(date(2022,1,1), date(2022, 2, 28))
    assert result == 2


def test_count_months_partial_first_month():
    result = dates.count_months_partial(date(2022,2,15), date(2022, 3, 31))
    assert result == 1.5


def test_count_months_partial_last_month():
    result = dates.count_months_partial(date(2022, 1, 1), date(2022, 4, 15))
    assert result == 3.5


def test_count_months_partial_two_partials():
    result = dates.count_months_partial(date(2022, 2, 15), date(2022, 4, 15))
    assert result == 2


def test_count_months_partial_two_partials_2():
    result = dates.count_months_partial(date(2022, 2, 22), date(2022, 4, 15))
    assert result == 1.75


def test_count_months_partial_two_partials_3():
    result = dates.count_months_partial(date(2022, 1, 2), date(2022, 4, 15))
    assert abs(result - 2.5 - (30/31)) < 0.01
