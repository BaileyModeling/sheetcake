from .cell import Cell
from typing import List, Callable
from sheetcake2.src.utils import is_number


class RoundCell(Cell):
    def __init__(self, value = None, num_digits: int = 0, name: str = "RoundCell", tolerance = 0.0, fmt: Callable = str, callback: Callable = None, locked: bool = False, validation_rules: List[Callable] = None) -> None:
        self.num_digits = num_digits
        super().__init__(value = value, name=name, tolerance=tolerance, fmt=fmt, callback=callback, locked=locked, validation_rules=validation_rules)

    def calculate(self):
        result = super().calculate()
        if result is not None:
            return round(result, self.num_digits)
        return None

    def formula(self, deep: bool = False):
        if len(self.operations) == 1 and self.operations[0][0] == "=" and is_number(self.operations[0][1]):
            return f"round( {self.fmt(self.operations[0][1])}, {self.num_digits} )"
        result = super().formula(deep=deep)
        return f"round( {result}, {self.num_digits} )"
