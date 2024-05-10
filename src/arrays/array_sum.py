from sheetcake import Array, SumCell, Cell
from typing import List, Callable
from sheetcake.src import errors


class ArraySum(Array):

    def __init__(self, arrays: List[Array], name="ArraySum", duration=None, tolerance = 0.0, fmt: Callable = str, callback: Callable = None, locked: bool = False, validation_rules: List[Callable] = None):
        self.arrays = arrays
        # self.tolerance = tolerance
        # self.fmt = fmt
        # self.callback = callback
        # self.locked = locked
        # self.validation_rules = validation_rules
        if not arrays and not duration:
            raise errors.ImproperConfig("ArraySum must have at least one array or a duration")
        if arrays:
            duration = len(arrays[0])

        for array in arrays:
            if not len(array) == duration:
                raise errors.ImproperConfig(f"Cannot add arrays of different length: {len(array)}, {duration}")
        array_sum = []
        # if not arrays:
        #     return super().__init__(array=array_sum, name=name)

        for col in range(duration):
            cell = SumCell(cells=[row[col] for row in arrays], name=f"{name}[{col}]", tolerance=tolerance, fmt=fmt, callback=callback, locked=locked, validation_rules=validation_rules)
            array_sum.append(cell)
        super().__init__(array=array_sum, name=name)

    def add(self, other):
        # if self.arrays and not (len(other) == len(self.arrays[0])):
        if not len(other) == self.duration:
            raise errors.ImproperConfig(f"Cannot add arrays of different length: {len(other)}, {len(self.arrays[0])}")
        # if not self.array:
        #     # self.array = Array.blank(num_cols=len(other), name=self.name)
        #     self.array = Array(array=list(SumCell(cells=[], name=f"{self.name}[{col}]", tolerance=self.tolerance, fmt=self.fmt, callback=self.callback, locked=self.locked, validation_rules=self.validation_rules) for col in range(len(other))), name=self.name)
        #     for cell in other:
        #         self.total.add(cell)
        self.arrays.append(other)
        for i, cell in enumerate(other):
            self.array[i].add(cell)
            # self.total.add(cell)
        # return super().add(other)

    def __repr__(self) -> str:
        return f"ArraySum({repr(self.arrays)}, name={self.name})"
