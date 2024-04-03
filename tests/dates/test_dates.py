from datetime import date, timedelta
from sheetcake import dates


def test_today():
    dates.today()
    assert True


def test_today_str():
    dates.today_str()
    assert True


def test_str_to_date():
    result = dates.str_to_date("2022-01-01")
    assert result == date(2022, 1, 1)


def test_str_to_date_slashes():
    result = dates.str_to_date("1/1/2022")
    assert result == date(2022, 1, 1)


def test_str_to_date_none():
    result = dates.str_to_date(None)
    assert result is None


def test_str_to_date_with_date():
    result = dates.str_to_date(date(2022, 1, 1))
    assert result == date(2022, 1, 1)


def test_days_to_timedelta():
    result = dates.days_to_timedelta(10)
    assert result == timedelta(days=10)


def test_days_to_timedelta_with_timedelta_arg():
    result = dates.days_to_timedelta(timedelta(days=10))
    assert result == timedelta(days=10)


def test_days_to_timedelta_zero():
    result = dates.days_to_timedelta(0)
    assert result == timedelta(days=0)


def test_count_days():
    result = dates.count_days(date(2022,1,1), date(2022, 1, 11))
    assert result == 10


def test_count_days_zero():
    result = dates.count_days(date(2022,1,1), date(2022, 1, 1))
    assert result == 0


def test_count_days_inclusive():
    result = dates.count_days(date(2022,1,1), date(2022, 1, 11), inclusive=True)
    assert result == 11


def test_count_months():
    result = dates.count_months(date(2022,1,15), date(2022, 2, 28))
    assert result == 1


def test_count_months_same_month():
    result = dates.count_months(date(2022, 1, 15), date(2022, 1, 28))
    assert result == 0


def test_count_months_negative():
    result = dates.count_months(date(2022, 2, 28), date(2022, 1, 15))
    assert result == -1


def test_previous_quarter_one():
    result = dates.previous_quarter(date(2022, 4, 1))
    assert result == date(2022, 3, 31)


def test_previous_quarter_two():
    result = dates.previous_quarter(date(2022, 7, 1))
    assert result == date(2022, 6, 30)


def test_previous_quarter_three():
    result = dates.previous_quarter(date(2022, 10, 1))
    assert result == date(2022, 9, 30)


def test_previous_quarter_four():
    result = dates.previous_quarter(date(2023, 1, 1))
    assert result == date(2022, 12, 31)


def test_eomonth_30():
    result = dates.eomonth(date(2022, 6, 1))
    assert result == date(2022, 6, 30)


def test_eomonth_31():
    result = dates.eomonth(date(2022, 1, 1))
    assert result == date(2022, 1, 31)


def test_eomonth_leap_year():
    result = dates.eomonth(date(2020, 2, 1))
    assert result == date(2020, 2, 29)


def test_eomonth_non_leap_year():
    result = dates.eomonth(date(2022, 2, 1))
    assert result == date(2022, 2, 28)


def test_eoyear():
    result = dates.eoyear(date(2022, 6, 1))
    assert result == date(2022, 12, 31)


def test_boyear():
    result = dates.boyear(date(2022, 6, 1))
    assert result == date(2022, 1, 1)


def test_eoquarter_one():
    result = dates.eoquarter(date(2022, 1, 1))
    assert result == date(2022, 3, 31)


def test_eoquarter_two():
    result = dates.eoquarter(date(2022, 4, 1))
    assert result == date(2022, 6, 30)


def test_eoquarter_three():
    result = dates.eoquarter(date(2022, 7, 1))
    assert result == date(2022, 9, 30)


def test_eoquarter_four():
    result = dates.eoquarter(date(2022, 10, 1))
    assert result == date(2022, 12, 31)


def test_add_day():
    result = dates.add_day(date(2022, 2, 28), days=2)
    assert result == date(2022, 3, 2)


def test_next_day():
    result = dates.next_day(date(2022, 2, 28))
    assert result == date(2022, 3, 1)


def test_days_in_month():
    result = dates.days_in_month(date(2022,1,1))
    assert result == 31


def test_days_in_year():
    result = dates.days_in_year(date(2022,1,1))
    assert result == 365


def test_days_in_year_leapyear():
    result = dates.days_in_year(date(2020,1,1))
    assert result == 366


def test_remaining_days():
    result = dates.remaining_days(date(2022,1,1))
    assert result == 31


def test_remaining_days_leapyear():
    result = dates.remaining_days(date(2020,2,1))
    assert result == 29


def test_pct_remaining_days():
    result = dates.pct_remaining_days(date(2022,2,15))
    assert abs(result - 0.5) < 0.001


def test_pct_days_passed():
    result = dates.pct_days_passed(date(2022,2,15))
    assert abs(result - 0.5) < 0.001


def test_beginning_of_month():
    result = dates.beginning_of_month(date(2020,2,29))
    assert result == date(2020, 2, 1)


def test_is_beginning_of_month():
    result = dates.is_beginning_of_month(date(2020,2,1))
    assert result


def test_is_beginning_of_month_false():
    result = dates.is_beginning_of_month(date(2020,2,29))
    assert not result


def test_is_end_of_month():
    result = dates.is_end_of_month(date(2020,2,29))
    assert result


def test_is_end_of_month_false():
    result = dates.is_end_of_month(date(2020,2,1))
    assert not result


def test_is_same_month():
    result = dates.is_same_month(date(2022, 1, 1), date(2022, 1, 31))
    assert result


def test_is_same_month_false():
    result = dates.is_same_month(date(2022, 1, 1), date(2022, 2, 1))
    assert not result


def test_to_quarter_one():
    result = dates.to_quarter(date(2022, 1, 1))
    assert result == "Q1 2022"


def test_to_quarter_two():
    result = dates.to_quarter(date(2022, 4, 1))
    assert result == "Q2 2022"


def test_to_quarter_three():
    result = dates.to_quarter(date(2022, 7, 1))
    assert result == "Q3 2022"


def test_to_quarter_four():
    result = dates.to_quarter(date(2022, 10, 1))
    assert result == "Q4 2022"


def test_daterange():
    result = [dt for dt in dates.daterange(date(2020,2,28), date(2022,3,1))]
    assert result[0] == date(2020,2,28)
    assert result[1] == date(2020,2,29)
    assert result[2] == date(2020,3,1)


def test_monthlyrange():
    result = [dt for dt in dates.monthlyrange(date(2022,1,1), date(2022,3,1))]
    assert result[0] == date(2022,1,1)
    assert result[1] == date(2022,2,1)
    assert result[2] == date(2022,3,1)

def test_prorate():
    assert abs(dates.prorate(100, date(2022, 2, 15), inclusive=False) - 50) < 0.01

def test_prorate_inclusive():
    assert abs(dates.prorate(100, date(2022, 2, 14), inclusive=True) - 50) < 0.01


def test_count_years():
    assert dates.count_years(date(2022,1,1), date(2022,12,31)) == 0
    assert dates.count_years(date(2022,1,1), date(2023,1,1)) == 1
    assert dates.count_years(date(2022,12,31), date(2023,1,1)) == 1
