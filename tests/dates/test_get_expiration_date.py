from datetime import date
from sheetcake2 import dates


def test_get_expiration_date():
    result = dates.get_expiration_date(date(2022,1,1), 12, end_of_month=True)
    assert result == date(2022, 12, 31)


def test_get_expiration_date_eom_false():
    result = dates.get_expiration_date(date(2022,1,1), 12, end_of_month=False)
    assert result == date(2022, 12, 31)


def test_get_expiration_date_mid_month():
    result = dates.get_expiration_date(date(2022,1,2), 12, end_of_month=True)
    assert result == date(2023, 1, 31)


def test_get_expiration_date_eom_false_mid_month():
    result = dates.get_expiration_date(date(2022,1,2), 12, end_of_month=False)
    assert result == date(2023, 1, 1)
