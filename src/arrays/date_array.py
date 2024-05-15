import numpy as np
import datetime as dt
from sheetcake import DateRow, Row, fmt
from sheetcake.src.dates import str_to_date, beginning_of_month, relativedelta, eomonth, days_in_year, count_days
from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class DateArray:
    """
    Date Array holds lists of dates for a timeseries: start, end, days, month, year, ndarray
    """
    start_date: dt.date
    duration: int

    def __post_init__(self) -> None:
        self.start_date = str_to_date(self.start_date)
        if self.duration < 1:
            raise ValueError(f"duration must be integer 1 or greater: {self.duration}")

        self.start = DateRow.from_values(
            values=list(beginning_of_month(self.start_date) + relativedelta(months=i) for i in range(self.duration)),
            name="Start Date",
            fmt=fmt.date,
        )
        self.end = DateRow.from_values(values=list(eomonth(dt) for dt in self.start.values), name="End Date", fmt=fmt.date)
        self.days = Row.from_values(values=list((self.end.get_value(i) - self.start.get_value(i)).days + 1 for i in range(self.duration)), name="Days in Period", fmt=fmt.comma)
        self.month = Row.from_values(values=list((col.month for col in self.start.values)), name="Month", fmt=fmt.comma)
        self.year = Row.from_values(values=list((col.year for col in self.start.values)), name="Year", fmt=fmt.comma)
        self.quarter = Row.from_values(values=list((1+(col.month-1)//3 for col in self.start.values)), name="Quarter", fmt=fmt.comma)
        self.ndarray = np.array(self.start.values, dtype='datetime64')
        self.days_in_year = Row.from_values(values=list(days_in_year(dt) for dt in self.start.values), name="Days in Year", fmt=fmt.comma)
        self.years = sorted(list(set(self.year.values)))
        self.year_indicies = self.get_year_indicies()
        self.quarters = self.get_qtr_list()
        self.qtr_indicies = self.get_qtr_indicies()
        self.qtr_and_yr = self.get_qtr_and_yr_list()
        self.qtr_and_yr_indicies = self.get_qtr_and_yr_indicies()

    def __getitem__(self, i):
        return self.end[i]

    @property
    def debug_dict(self) -> dict:
        return self.__dict__

    @property
    def end_date(self) -> dt.date:
        return self.end[-1].value

    def index_ym(self, year: int, month: int) -> int:
        """
        Return array index for a given year and month.
        """
        result = 12 * (year - self.start_date.year)
        result += month - self.start_date.month
        return result

    def index(self, date: dt.date) -> int:
        """
        Return array index for a given dt.date.
        """
        result = 12 * (date.year - self.start_date.year)
        result += date.month - self.start_date.month
        return result

    def get_qtr_list(self) -> List[str]:
        """
        Return list of quarters formatted as 2023 Q1.
        """
        result = list(f"{dt.year} Q{1+(dt.month-1)//3}" for dt in self.end.values)
        return sorted(list(set(result)))
    
    def get_qtr_and_yr_list(self) -> List[str]:
        """
        Return list of quarters formatted as '2023 Q1' with annual totals '2023 Total'.
        """
        result = []
        prior_qtr = 0
        for dt in self.end.values:
            qtr = 1+(dt.month-1)//3
            yr = dt.year
            if qtr != prior_qtr:
                result.append(f"{yr} Q{qtr}")
                prior_qtr = qtr
            if dt.month == 12:
                result.append(f"{yr} Total")
        return result
    
    def get_qtr_and_yr_indicies(self) -> List[Tuple[int, int]]:
        """
        Return list of tuples of (start, end) indicies for each quarter and year.
        """
        result = []
        prior_qtr = 0
        prior_qtr_start = 0
        prior_yr = 0
        prior_yr_start = 0
        for i, dt in enumerate(self.end.values):
            qtr = 1+(dt.month-1)//3
            yr = dt.year
            if i == 0:
                prior_qtr = qtr
                prior_yr = yr
                continue
            if qtr != prior_qtr:
                result.append((prior_qtr_start, i))
                prior_qtr_start = i
                prior_qtr = qtr
            if yr != prior_yr:
                result.append((prior_yr_start, i))
                prior_yr_start = i
                prior_yr = yr
        result.append((prior_qtr_start, i+1))
        result.append((prior_yr_start, i+1))
        return result

    def get_qtr_indicies(self) -> List[Tuple[int, int]]:
        """
        Return list of tuples of (start, end) indicies for each quarter.
        """
        result = []
        prior_qtr = 0
        prior_qtr_start = 0
        for i, qtr in enumerate(self.quarter.values):
            if i == 0:
                prior_qtr = qtr
                continue
            if qtr != prior_qtr:
                result.append((prior_qtr_start, i))
                prior_qtr_start = i
                prior_qtr = qtr
        result.append((prior_qtr_start, i+1))
        return result

    def get_year_indicies(self) -> List[Tuple[int, int]]:
        """
        Return list of tuples of (start, end) indicies for each year.
        """
        result = []
        prior_year = 0
        prior_year_start = 0
        for i, yr in enumerate(self.year.values):
            if i == 0:
                prior_year = yr
                continue
            if yr != prior_year:
                result.append((prior_year_start, i))
                prior_year_start = i
                prior_year = yr
        result.append((prior_year_start, i+1))
        return result

    def year_index(self, year: int, inclusive: bool = False) -> Tuple[int, int]:
        """
        Return tuple of start, end for the given year.
        This used to be called year_incidies() but was renamed to year_index() on 7/15/23.
        """
        start = None
        end = None
        for i, yr in enumerate(self.year.values):
            if yr == year:
                start = i
                break
        for i, yr in enumerate(reversed(self.year.values)):
            if yr == year:
                end = self.duration - i
                if not inclusive:
                    end -= 1
                break
        return start, end
    
    def __eq__(self, other: object) -> bool:
        if not hasattr(other, "start_date") or not hasattr(other, "duration"):
            return False
        return self.start_date==other.start_date and self.duration==other.duration
    
    def prorated_days(self, end_date: dt.date) -> List[int]:
        """
        Return the number of days in the month for the given end_date.
        """
        return list(
            max(
                0, 
                min(
                    count_days(self.start.get_value(i), end_date, inclusive=False),
                    self.days.get_value(i)
                )
            ) for i in range(self.duration)
        )
