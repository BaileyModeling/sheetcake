from ..cells.cell import Cell
from typing import Callable, List


class Row:
    def __init__(self, cells: List[Cell], name: str) -> None:
        self.name = name
        self.cells = cells

    def __getitem__(self, i) -> Cell:
        return self.cells[i]
    
    def __len__(self) -> int:
        return len(self.cells)

    def __iter__(self):
        self.n = 0
        return self

    def __next__(self):
        if self.n < len(self.cells):
            result = self.cells[self.n]
            self.n += 1
            return result
        else:
            raise StopIteration

    def get_value(self, i: int):
        return self.cells[i].value

    def append(self, cell: Cell):
        self.cells.append(cell)

    @property
    def values(self) -> List:
        return [cell.value for cell in self.cells]

    @classmethod
    def from_values(cls, values: List, name: str, fmt: Callable = str, callback: Callable = None, locked: bool = False, validation_rules: List[Callable] = None) -> "Row":
        """
        Construct a row from a list of values.
        """
        cells = [Cell(value=value, name=f"{name}[{i}]", fmt=fmt, callback=callback, locked=locked, validation_rules=validation_rules) for i, value in enumerate(values)]
        return cls(cells=cells, name=name)

    @classmethod
    def zeros(cls, num_cols: int, name: str, fmt: Callable = str, callback: Callable = None, locked: bool = False, validation_rules: List[Callable] = None) -> "Row":
        """
        Construct a row of Cells with zero values.
        """
        cells = [Cell(value=0, name=f"{name}[{i}]", fmt=fmt, callback=callback, locked=locked, validation_rules=validation_rules) for i in range(num_cols)]
        return cls(cells=cells, name=name)

    @classmethod
    def blank(cls, num_cols: int, name: str, fmt: Callable = str, callback: Callable = None, locked: bool = False, validation_rules: List[Callable] = None) -> "Row":
        """
        Construct a row of empty cells.
        """
        cells = [Cell(value=None, name=f"{name}[{i}]", fmt=fmt, callback=callback, locked=locked, validation_rules=validation_rules) for i in range(num_cols)]
        return cls(cells=cells, name=name)
