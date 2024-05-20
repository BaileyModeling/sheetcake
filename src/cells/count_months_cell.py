from typing import Callable, Dict, List
from .cell import Cell
from .date_cell import DateCell
from sheetcake import dates


class CountMonthsCell(Cell):

    def __init__(self, start_date: DateCell, end_date: DateCell, name: str = "<CountMonthsCell>", fmt: Callable = str, callback: Callable = None, validation_rules: List[Callable] = None, meta_data: Dict = None) -> None:
        self.start_date = start_date
        self.end_date = end_date
        tolerance = 0
        locked = False
        super().__init__(value=None, name=name, tolerance=tolerance, fmt=fmt, callback=callback, locked=locked, validation_rules=validation_rules, meta_data=meta_data)
        if hasattr(end_date, 'changed'):
            end_date.changed.connect(self.update)
        if hasattr(start_date, 'changed'):
            start_date.changed.connect(self.update)
        self.operations.append(("=", end_date))
        self.operations.append(("-", start_date))
        self.update()

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        print(f"Cannot set value of count months cell {self.name} to {value}")
        return None

    def calculate(self):
        """
        Override this method to implement custom calculations
        """
        return dates.count_months(self.start_date.value, self.end_date.value)
