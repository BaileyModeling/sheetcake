from sheetcake.src import errors
from sheetcake import Cell
from sheetcake.src.arrays.base_array import BaseArray
from decimal import Decimal


class Array(BaseArray):
    def __init__(self, duration=None, name='Unnamed Array', array=None, fmt=None):
        super().__init__(duration, name, array, fmt)
        self.total_cell = Cell(None, name=f'{name} Total', fmt=fmt)
        self.total_cell.sum(*self._array)

    def __repr__(self):
        '''Returns representation of the object'''
        if self.fmt is not None:
            fmt = self.fmt.__name__
        else:
            fmt = self.fmt
        cls_name = self.__class__.__name__
        return f"{cls_name}({self.duration}, {self.name}, {self._array}, {fmt})"

    @property
    def total(self):
        return self.total_cell.value

    @staticmethod
    def sum(*args, name='Unnamed Array', fmt=None, duration=None):
        if len(args):
            duration = len(args[0])
        if duration is None:
            raise errors.ImproperConfig("Must set either args or duration.")
        result = Array(duration=duration, name=name, fmt=fmt)
        for array in args:
            if not len(array) == duration:
                raise ValueError(f"Cannot add arrays of different length: {len(array)}, {duration}")
            for i, cell in enumerate(array):
                result[i].add(cell)
        return result

    @staticmethod
    def sub_all(*args, name='Unnamed Array', fmt=None, duration=None):
        if len(args):
            duration = len(args[0])
        if duration is None:
            raise errors.ImproperConfig("Must set either args or duration.")
        result = Array(duration=duration, name=name, fmt=fmt)
        for array in args:
            if not len(array) == duration:
                raise ValueError(f"Cannot add arrays of different length: {len(array)}, {duration}")
            for i, cell in enumerate(array):
                result[i].sub(cell)
        return result

    def print(self):
        for cell in self._array:
            cell.print()

    def print_cells(self):
        for i, cell in enumerate(self._array):
            print(i, ": ", repr(cell))

    def add(self, *args):
        for array in args:
            if not len(array) == self.duration:
                raise ValueError(f"Cannot add arrays of different length: {len(array)}, {self.duration}")
            for i, cell in enumerate(array):
                self[i].add(cell)
    
    def sub(self, *args):
        for array in args:
            if not len(array) == self.duration:
                raise ValueError(f"Cannot subtract arrays of different length: {len(array)}, {self.duration}")
            for i, cell in enumerate(array):
                self[i].sub(cell)

    def __add__(self, other):
        array = Array(duration=self.duration, fmt=self.fmt)
        if isinstance(other, BaseArray):
            if not len(self) == len(other):
                raise ValueError(f"Cannot add arrays of different length: {len(self)}, {len(other)}")
            other_name = other.name
            for i, cell in enumerate(array):
                cell.add(self[i])
                cell.add(other[i])
        elif isinstance(other, (int, float, Decimal, Cell)):
            other_name = str(other)
            for i, cell in enumerate(array):
                cell.add(self[i])
                cell.add(other)
        else:
            raise TypeError(f"Cannot add type {type(self)} and {type(other)}")
        array.name = self.name + " + " + other_name
        return array

    __radd__ = __add__

    def __sub__(self, other):
        array = Array(duration=self.duration, fmt=self.fmt)
        if isinstance(other, BaseArray):
            if not len(self) == len(other):
                raise ValueError(f"Cannot add arrays of different length: {len(self)}, {len(other)}")
            for i, cell in enumerate(array):
                cell.add(self[i])
                cell.sub(other[i])
        elif isinstance(other, (int, float, Decimal, Cell)):
            for i, cell in enumerate(array):
                cell.add(self[i])
                cell.sub(other)
        else:
            raise TypeError(f"Cannot subtract type {type(self)} and {type(other)}")
        return array

    def __rsub__(self, other):
        if isinstance(other, BaseArray):
            if not len(self) == len(other):
                raise ValueError(f"Cannot add arrays of different length: {len(self)}, {len(other)}")
            array = Array(duration=self.duration, fmt=self.fmt)
            for i, cell in enumerate(array):
                cell.add(other[i])
                cell.sub(self[i])
        elif isinstance(other, (int, float, Decimal, Cell)):
            array = Array(array=[other]*self.duration, fmt=self.fmt)
            for i, cell in enumerate(array):
                cell.sub(self[i])
        else:
            raise TypeError(f"Cannot subtract type {type(self)} and {type(other)}")
        return array

    def __mul__(self, other):
        array = Array(duration=self.duration, fmt=self.fmt)
        if isinstance(other, BaseArray):
            if not len(self) == len(other):
                raise ValueError(f"Cannot add arrays of different length: {len(self)}, {len(other)}")
            for i, cell in enumerate(array):
                cell.add(self[i])
                cell.mult(other[i])
        elif isinstance(other, (int, float, Decimal, Cell)):
            for i, cell in enumerate(array):
                cell.add(self[i])
                cell.mult(other)
        else:
            raise TypeError(f"Cannot multiply type {type(self)} and {type(other)}")
        return array

    __rmul__ = __mul__

    def __div__(self, other):
        array = Array(duration=self.duration, fmt=self.fmt)
        if isinstance(other, BaseArray):
            if not len(self) == len(other):
                raise ValueError(f"Cannot add arrays of different length: {len(self)}, {len(other)}")
            for i, cell in enumerate(array):
                cell.add(self[i])
                cell.div(other[i])
        elif isinstance(other, (int, float, Decimal, Cell)):
            for i, cell in enumerate(array):
                cell.add(self[i])
                cell.div(other)
        else:
            raise TypeError(f"Cannot divide type {type(self)} and {type(other)}")
        return array

    __truediv__ = __div__

    def __rdiv__(self, other):
        array = Array(duration=self.duration, fmt=self.fmt)
        if isinstance(other, BaseArray):
            if not len(self) == len(other):
                raise ValueError(f"Cannot add arrays of different length: {len(self)}, {len(other)}")
            for i, cell in enumerate(array):
                cell.add(other[i])
                cell.div(self[i])
        elif isinstance(other, (int, float, Decimal, Cell)):
            for i, cell in enumerate(array):
                cell.add(other)
                cell.div(self[i])
        else:
            raise TypeError(f"Cannot divide type {type(self)} and {type(other)}")
        return array

    __rtruediv__ = __rdiv__

    def __neg__(self):
        # array = Array(array=[-1]*self.duration, fmt=self.fmt)
        # return array * self
        # print([-1*i for i in self._array])
        return Array(array=[-1*i for i in self._array], name=f"-1*{self.name}", fmt=self.fmt)


def zeros(duration, name="Unnamed Array", fmt=None):
    return Array(name=name, array=[0]*duration, fmt=fmt)


def array_sum(arrays, name="Unnamed Array", fmt=None):
    duration = len(arrays[0])
    array = Array(duration=duration, name=name, fmt=fmt)
    for arr in arrays:
        array += arr
    # array = sum(arrays)
    # array.name = name
    # array.fmt = fmt
    return array
