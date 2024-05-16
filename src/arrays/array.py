from typing import Callable, List
from decimal import Decimal
import numpy as np
from sheetcake import Cell, SumCell, MaxCell, MinCell
from sheetcake.src.utils import is_number, is_iterable
from sheetcake.src.fmt import comma2
from sheetcake.src.vector import is_scalar, is_vector


class Array:
    default_name = "Array"

    def __init__(self, array: List[Cell], name: str = "", fmt: Callable = None) -> None:
        self.name = name or self.default_name
        self.array = array
        default_fmt = array[0].fmt if array else comma2
        self.fmt = fmt or default_fmt
        self.total = SumCell(self.array, name=f"{name} Total", fmt=self.fmt)

    @property
    def columns(self) -> List[Cell]:
        return self.array
    
    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Array({repr(self.array)}, name={self.name})"

    def __getitem__(self, i) -> Cell:
        if i == len(self.array):
            return self.total
        return self.columns[i]

    def __len__(self) -> int:
        return len(self.array)

    def __iter__(self):
        self.n = 0
        return self

    def __next__(self):
        if self.n < self.duration:
            result = self.array[self.n]
            self.n += 1
            return result
        else:
            raise StopIteration

    @property
    def duration(self):
        return len(self.array)

    def append(self, cell: Cell):
        self.array.append(cell)
        self.total.add_cell(cell)

    def set_value(self, i, value):
        self.array[i].value = value

    def get_value(self, i):
        return self.array[i].value

    def set_values(self, array, start:int=0):
        for i, value in enumerate(array):
            self.array[start + i].value = value

    def print(self):
        print(self.name)
        for i, cell in enumerate(self.array):
            print(f"\t{i:<3}: {str(cell)}")

    def print_cells(self, width: int = 15):
        for cell in self.array:
            cell.print(width=width)

    def print_row(self, seperator: str = " | "):
        result = seperator.join(list(str(cell) for cell in self.array))
        print(result)

    def print_formulas(self, width: int = 15, deep: bool = False):
        for cell in self.array:
            print(f"{cell.name:<{width}}: {cell.formula(deep=deep)}")

    def print_value_audit(self, width: int = 15, deep: bool = False):
        for cell in self.array:
            print(f"{cell.name:<{width}}: {cell.value_audit(deep=deep)}")

    def _is_compatible(self, other) -> bool:
        return len(self.array) == len(other)

    def equal(self, other):
        if is_vector(other):
            if not self._is_compatible(other):
                raise TypeError(f"Cannot equal arrays of different length: {len(self.array)}, {len(other)}")
            for i, cell in enumerate(other):
                self.array[i].equal_cell(cell)
        elif is_scalar(other):
            for cell in self.array:
                cell.equal_cell(other)
        else:
            raise TypeError(f"Cannot equal type {type(self)} and {type(other)}")
        return self

    def add(self, other):
        if is_vector(other):
            if not self._is_compatible(other):
                raise TypeError(f"Cannot add arrays of different length: {len(self.array)}, {len(other)}")
            for i, cell in enumerate(other):
                self.array[i].add_cell(cell)
        elif is_scalar(other):
            for cell in self.array:
                cell.add_cell(other)
        else:
            raise TypeError(f"Cannot add type {type(self)} and {type(other)}")
        return self

    def mult(self, other):
        if is_vector(other):
            if not self._is_compatible(other):
                raise TypeError(f"Cannot mult arrays of different length: {len(self.array)}, {len(other)}")
            for i, cell in enumerate(other):
                self.array[i].mult_cell(cell)
        elif is_scalar(other):
            for cell in self.array:
                cell.mult_cell(other)
        else:
            raise TypeError(f"Cannot mult type {type(self)} and {type(other)}")
        return self

    @classmethod
    def sum(cls, arrays: List["Array"], name: str = None, tolerance = 0.0, fmt: Callable = str, callback: Callable = None, locked: bool = False, validation_rules: List[Callable] = None) -> "Array":
        """
        Construct an Array that is the sum of a list of arrays.
        """
        name = name or cls.default_name
        array = []
        for col in range(len(arrays[0])):
            cell = SumCell(cells=[row[col] for row in arrays], name=f"{name}[{col}]", tolerance=tolerance, fmt=fmt, callback=callback, locked=locked, validation_rules=validation_rules)
            array.append(cell)
        return cls(array=array, name=name)

    @classmethod
    def from_values(cls, values: List, name: str = None, fmt: Callable = str, tolerance = 0.0, callback: Callable = None, locked: bool = False, validation_rules: List[Callable] = None) -> "Array":
        """
        Construct an Array from a list of values.
        """
        name = name or cls.default_name
        array = [Cell(value=value, name=f"{name}[{i}]", tolerance=tolerance, fmt=fmt, callback=callback, locked=locked, validation_rules=validation_rules) for i, value in enumerate(values)]
        return cls(array=array, name=name)

    @classmethod
    def zeros(cls, num_cols: int, name: str = None, fmt: Callable = str, tolerance = 0.0, callback: Callable = None, locked: bool = False, validation_rules: List[Callable] = None) -> "Array":
        """
        Construct an Array with zero values.
        """
        name = name or cls.default_name
        array = [Cell(value=0, name=f"{name}[{i}]", tolerance=tolerance, fmt=fmt, callback=callback, locked=locked, validation_rules=validation_rules) for i in range(num_cols)]
        return cls(array=array, name=name)

    @classmethod
    def blank(cls, num_cols: int, name: str = None, fmt: Callable = str, tolerance = 0.0, callback: Callable = None, locked: bool = False, validation_rules: List[Callable] = None) -> "Array":
        """
        Construct an Array of empty cells.
        """
        name = name or cls.default_name
        array = [Cell(value=None, name=f"{name}[{i}]", tolerance=tolerance, fmt=fmt, callback=callback, locked=locked, validation_rules=validation_rules) for i in range(num_cols)]
        return cls(array=array, name=name)
    
    @classmethod
    def max(cls, arrays: List["Array"], name: str = "MaxArray", tolerance = 0.0, fmt: Callable = str, callback: Callable = None, locked: bool = False, validation_rules: List[Callable] = None):
        """
        Construct an Array that is the max of a list of arrays.
        """
        name = name or cls.default_name
        iterables = [array for array in arrays if is_iterable(array)]
        scalar = [array for array in arrays if is_scalar(array)]
        array = []
        for col in range(len(iterables[0])):
            cell = MaxCell(cells=[row[col] for row in iterables]+scalar, name=f"{name}[{col}]", tolerance=tolerance, fmt=fmt, callback=callback, locked=locked, validation_rules=validation_rules)
            array.append(cell)
        return cls(array=array, name=name)

    def __add__(self, other):
        array = Array.blank(num_cols=len(self), fmt=self.fmt)
        if is_vector(other):
            if not len(self) == len(other):
                raise ValueError(f"Cannot add arrays of different length: {len(self)}, {len(other)}")
            other_name = other.name
            for i, cell in enumerate(array):
                cell.add_cell(self[i])
                cell.add_cell(other[i])
        elif is_scalar(other):
            other_name = str(other)
            for i, cell in enumerate(array):
                cell.add_cell(self[i])
                cell.add_cell(other)
        else:
            raise TypeError(f"Cannot add type {type(self)} and {type(other)}")
        array.name = self.name + " + " + other_name
        return array

    __radd__ = __add__

    def __sub__(self, other):
        array = Array.blank(num_cols=len(self), fmt=self.fmt)
        if is_vector(other):
            if not len(self) == len(other):
                raise ValueError(f"Cannot add arrays of different length: {len(self)}, {len(other)}")
            for i, cell in enumerate(array):
                cell.add_cell(self[i])
                cell.sub_cell(other[i])
        elif is_scalar(other):
            for i, cell in enumerate(array):
                cell.add_cell(self[i])
                cell.sub_cell(other)
        else:
            raise TypeError(f"Cannot subtract type {type(self)} and {type(other)}")
        return array

    def __rsub__(self, other):
        array = Array.blank(num_cols=len(self), fmt=self.fmt)
        if is_vector(other):
            if not len(self) == len(other):
                raise ValueError(f"Cannot add arrays of different length: {len(self)}, {len(other)}")
            for i, cell in enumerate(array):
                cell.add_cell(other[i])
                cell.sub_cell(self[i])
        elif is_scalar(other):
            for i, cell in enumerate(array):
                cell.add_cell(other)
                cell.sub_cell(self[i])
        else:
            raise TypeError(f"Cannot subtract type {type(self)} and {type(other)}")
        return array

    def __neg__(self):
        return Array(array=[-1*cell for cell in self.array], name=f"-1*{self.name}")

    def __mul__(self, other):
        array = Array.blank(num_cols=len(self), fmt=self.fmt)
        if is_vector(other):
            if not len(self) == len(other):
                raise ValueError(f"Cannot add arrays of different length: {len(self)}, {len(other)}")
            for i, cell in enumerate(array):
                cell.add_cell(self[i])
                cell.mult_cell(other[i])
        elif is_scalar(other):
            for i, cell in enumerate(array):
                cell.add_cell(self[i])
                cell.mult_cell(other)
        else:
            raise TypeError(f"Cannot multiply type {type(self)} and {type(other)}")
        return array

    __rmul__ = __mul__

    def __div__(self, other):
        array = Array.blank(num_cols=len(self), fmt=self.fmt)
        if is_vector(other):
            if not len(self) == len(other):
                raise ValueError(f"Cannot add arrays of different length: {len(self)}, {len(other)}")
            for i, cell in enumerate(array):
                cell.add_cell(self[i])
                cell.div_cell(other[i])
        elif is_scalar(other):
            for i, cell in enumerate(array):
                cell.add_cell(self[i])
                cell.div_cell(other)
        else:
            raise TypeError(f"Cannot divide type {type(self)} and {type(other)}")
        return array

    __truediv__ = __div__

    def __rdiv__(self, other):
        array = Array.blank(num_cols=len(self), fmt=self.fmt)
        if is_vector(other):
            if not len(self) == len(other):
                raise ValueError(f"Cannot add arrays of different length: {len(self)}, {len(other)}")
            for i, cell in enumerate(array):
                cell.add_cell(other[i])
                cell.div_cell(self[i])
        elif is_scalar(other):
            for i, cell in enumerate(array):
                cell.add_cell(other)
                cell.div_cell(self[i])
        else:
            raise TypeError(f"Cannot divide type {type(self)} and {type(other)}")
        return array

    __rtruediv__ = __rdiv__
