from typing import Callable, List
from .array import Array
from sheetcake import Cell, SumCell, DateArray
from sheetcake.src.vector import is_scalar, is_vector


class TimeSeries(Array):
    default_name = "Time Series"

    def __init__(self, date_array: DateArray, array: List[Cell], name: str = "", fmt: Callable = str) -> None:
        self.date_array = date_array
        super().__init__(array=array, name=name, fmt=fmt)
        if len(self) != date_array.duration:
            raise ValueError(f"Array length {len(self)} does not match date_array duration {date_array.duration}")

    def __repr__(self):
        return f"TimeSeries(date_array={repr(self.date_array)}, array={repr(self.array)}, name={self.name})"

    def print(self):
        print(self.name)
        for i, cell in enumerate(self.array):
            print(f"  {i:<3}: {self.date_array[i]} : {str(cell)}")

    def _is_compatible(self, other) -> bool:
        if hasattr(other, "date_array") and not self.date_array == other.date_array:
            return False
        if len(self) != len(other):
            return False
        return True

    def __add__(self, other):
        array = TimeSeries.blank(date_array=self.date_array, fmt=self.fmt)
        if is_vector(other):
            if not self._is_compatible(other):
                raise ValueError(f"Cannot add timeseries of different length: {len(self)}, {len(other)}")
            other_name = other.name
            for i, cell in enumerate(array):
                cell.add(self[i])
                cell.add(other[i])
        elif is_scalar(other):
            other_name = str(other)
            for i, cell in enumerate(array):
                cell.add(self[i])
                cell.add(other)
        else:
            raise TypeError(f"Cannot add type {type(self)} and {type(other)}")
        array.name = self.name + " + " + other_name
        return array

    __radd__ = __add__

    @classmethod
    def sum(cls, series: List["TimeSeries"], name: str = None, tolerance = 0.0, fmt: Callable = str, callback: Callable = None, locked: bool = False, validation_rules: List[Callable] = None) -> "TimeSeries":
        """
        Construct a TimeSeries that is the sum of a list of timeseries.
        """
        name = name or cls.default_name
        date_array = series[0].date_array
        array = []
        for col in range(len(series[0])):
            cell = SumCell(cells=[row[col] for row in series], name=f"{name}[{col}]", tolerance=tolerance, fmt=fmt, callback=callback, locked=locked, validation_rules=validation_rules)
            array.append(cell)
        return cls(date_array=date_array, array=array, name=name)

    @classmethod
    def from_values(cls, date_array: DateArray, values: List, name: str = None, fmt: Callable = str, tolerance = 0.0, callback: Callable = None, locked: bool = False, validation_rules: List[Callable] = None) -> "Array":
        """
        Construct an Array from a list of values.
        """
        name = name or cls.default_name
        array = [Cell(value=value, name=f"{name}[{i}]", tolerance=tolerance, fmt=fmt, callback=callback, locked=locked, validation_rules=validation_rules) for i, value in enumerate(values)]
        return cls(date_array=date_array, array=array, name=name, fmt=fmt)

    @classmethod
    def zeros(cls, date_array: DateArray, name: str = None, fmt: Callable = str, tolerance = 0.0, callback: Callable = None, locked: bool = False, validation_rules: List[Callable] = None) -> "Array":
        """
        Construct an Array with zero values.
        """
        name = name or cls.default_name
        array = [Cell(value=0, name=f"{name}[{i}]", tolerance=tolerance, fmt=fmt, callback=callback, locked=locked, validation_rules=validation_rules) for i in range(date_array.duration)]
        return cls(date_array=date_array, array=array, name=name, fmt=fmt)

    @classmethod
    def blank(cls, date_array: DateArray, name: str = None, fmt: Callable = str, tolerance = 0.0, callback: Callable = None, locked: bool = False, validation_rules: List[Callable] = None) -> "Array":
        """
        Construct a TimeSeries of empty cells.
        """
        name = name or cls.default_name
        array = [Cell(value=None, name=f"{name}[{i}]", tolerance=tolerance, fmt=fmt, callback=callback, locked=locked, validation_rules=validation_rules) for i in range(date_array.duration)]
        return cls(date_array=date_array, array=array, name=name, fmt=fmt)
