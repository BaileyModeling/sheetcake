import datetime
from dateutil.relativedelta import relativedelta
from decimal import Decimal
import numpy as np
from typing import Union, Iterator


# ===========================================================
# Date/Time
# ===========================================================
DateType = Union[datetime.datetime, datetime.date]
NumberType = Union[int, float, Decimal, np.number]


def today() -> datetime.date:
    """returns today's date as a date object"""
    return datetime.date.today()


def today_str() -> str:
    """returns today's date as a string yyyy-mm-dd"""
    return datetime.date.today().strftime('%F')


def str_to_date(date_string: Union[str, datetime.date]) -> datetime.date:
    """
    date_string: Y-m-d
    Returns datetime.date
    Returns None if date_string is None
    """
    if date_string is None:
        return None
    elif isinstance(date_string, datetime.date):
        return date_string
    elif '/' in date_string:
        return datetime.datetime.strptime(date_string, "%m/%d/%Y").date()
    else:
        # if date is formated as a string, then convert to datetime
        return datetime.datetime.strptime(date_string, "%Y-%m-%d").date()


def days_to_timedelta(days_int: int) -> datetime.timedelta:
    if isinstance(days_int, datetime.timedelta):
        return days_int
    else:
        return datetime.timedelta(days=days_int)


def count_days(start_date: DateType, end_date: DateType, inclusive: bool=False) -> int:
    """Count days between two dates. Exclude start date by default."""
    interval = end_date - start_date
    if inclusive:
        return interval.days + 1
    return interval.days


def count_months(start_date: DateType, end_date: DateType, day_of_month=1) -> int:
    """count months between two dates"""
    interval = (
        (end_date.year - start_date.year) * 12 + end_date.month - start_date.month
    )
    # todo:
    # if start_date.day <= day_of_month, then include start month in count
    # if end_date.day > day_of_month, then include end month in count
    return interval


def count_months_partial(turnover_date: DateType, expiration_date: DateType) -> NumberType:
    """Number of months in SLR term, including fractional months."""
    months = count_months(turnover_date, expiration_date)
    if not is_beginning_of_month(turnover_date):
        months += pct_remaining_days(turnover_date)
    else:
        months += 1
    if not is_end_of_month(expiration_date):
        # deduct remaining days AFTER expiration_date
        months -= pct_remaining_days(next_day(expiration_date))
    return months


def count_years(start_date: DateType, end_date: DateType) -> int:
    """count years between two dates"""
    return end_date.year - start_date.year


def previous_quarter(start_date: DateType) -> datetime.date:
    if start_date.month < 4:
        return datetime.date(start_date.year - 1, 12, 31)
    elif start_date.month < 7:
        return datetime.date(start_date.year, 3, 31)
    elif start_date.month < 10:
        return datetime.date(start_date.year, 6, 30)
    return datetime.date(start_date.year, 9, 30)


def eomonth(start_date: DateType, num_months: int=0) -> datetime.date:
    # updated 8/12/21 to fix num_months > 0
    next_month = start_date.replace(day=1) + relativedelta(months=num_months)
    next_month = next_month.replace(day=28) + datetime.timedelta(
        days=4
    )
    next_month = next_month - datetime.timedelta(days=next_month.day)
    return next_month


def edays(start_date: DateType, num_days: int) -> datetime.date:
    return start_date + datetime.timedelta(days=num_days)


def eoyear(start_date: datetime.date, num_years: int = 0) -> datetime.date:
    return datetime.date(start_date.year + num_years, 12, 31)


def boyear(start_date: datetime.date) -> datetime.date:
    return datetime.date(start_date.year, 1, 1)


def eoquarter(start_date: datetime.date) -> datetime.date:
    mo = start_date.month
    if mo <= 3:
        return datetime.date(start_date.year, 3, 31)
    elif mo <= 6:
        return datetime.date(start_date.year, 6, 30)
    elif mo <= 9:
        return datetime.date(start_date.year, 9, 30)
    else:
        return datetime.date(start_date.year, 12, 31)


def edate(start_date: DateType, num_months: int, inclusive: bool=True) -> datetime.date:
    m = (start_date.month + num_months) % 12
    if not m:
        m = 12
    y = start_date.year + ((start_date.month) + num_months - 1) // 12
    d = min(
        start_date.day,
        [
            31,
            29 if y % 4 == 0 and not y % 400 == 0 else 28,
            31,
            30,
            31,
            30,
            31,
            31,
            30,
            31,
            30,
            31,
        ][m - 1],
    )
    result = start_date.replace(day=d, month=m, year=y)
    if not inclusive:
        result = result - datetime.timedelta(days=1)
    return result


def add_day(date: datetime.date, days=1) -> datetime.date:
    return date + datetime.timedelta(days=days)


def next_day(date: datetime.date) -> datetime.date:
    return date + datetime.timedelta(days=1)


def days_in_month(date: datetime.date) -> int:
    return count_days(datetime.date(date.year, date.month, 1), eomonth(date, 0)) + 1


def days_in_year(date: datetime.date) -> int:
    start = datetime.date(date.year, 1, 1)
    end = datetime.date(date.year, 12, 31)
    return (end - start).days + 1


def remaining_days(date: datetime.date) -> int:
    """Remaining days in month including start date"""
    return count_days(date, eomonth(date, 0)) + 1


def pct_remaining_days(date: DateType) -> NumberType:
    """Percentage of remaining days in month including start date"""
    remain = count_days(date, eomonth(date, 0)) + 1
    total = count_days(datetime.date(date.year, date.month, 1), eomonth(date, 0)) + 1
    return remain / total


def pct_days_passed(date: DateType, inclusive=False) -> NumberType:
    """Percentage of days passed in month excluding end date"""
    passed = count_days(beginning_of_month(date), date)
    if inclusive:
        passed += 1
    total = count_days(datetime.date(date.year, date.month, 1), eomonth(date, 0)) + 1
    return passed / total


def beginning_of_month(date: datetime.date) -> datetime.date:
    """First day of month for a given date."""
    return datetime.date(date.year, date.month, 1)


def is_beginning_of_month(date: DateType) -> bool:
    return date.day == 1


def is_end_of_month(date: DateType) -> bool:
    return date == eomonth(date)


def is_same_month(date1: DateType, date2: DateType) -> bool:
    return date1.year == date2.year and date1.month == date2.month


def next_month(date=None) -> datetime.date:
    """First day of next month after given date."""
    if date is None:
        date = today()
    else:
        date = str_to_date(date)
    return beginning_of_month(edate(date, 1))


def to_quarter(date: datetime.date) -> str:
    """e.g. Q3 2019"""
    return f'Q{date.month // 3 + 1} {date.year}'


def get_expiration_date(commencement_date: datetime.date, term_months: int, end_of_month=True) -> datetime.date:
    if end_of_month:
        if not commencement_date.day == 1:
            commencement_date = next_month(commencement_date)
        return eomonth(commencement_date, term_months - 1)
    return add_day(edate(commencement_date, term_months), -1)


def daterange(start_date: datetime.date, end_date: datetime.date) -> Iterator[datetime.date]:
    """Generator of daily dates within the given range, inclusive of start and end."""
    for n in range(int((end_date - start_date).days)):
        yield start_date + datetime.timedelta(n)


def monthlyrange(start_date: datetime.date, end_date: datetime.date) -> Iterator[datetime.date]:
    """Generator of monthly dates (using edate) within the given range, inclusive of start and end."""
    for n in range(count_months(start_date, end_date) + 1):
        yield edate(start_date, n)


def eomonth_range(start_date: datetime.date, duration: int) -> Iterator[datetime.date]:
    """Generator of monthly dates (using eomonth) within the given range."""
    for n in range(duration):
        yield eomonth(start_date, n)


def prorate(amount: float, on_date: datetime.date, inclusive: bool = False) -> float:
    return amount * pct_days_passed(on_date, inclusive=inclusive)
