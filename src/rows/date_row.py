from ..cells.date_cell import DateCell
from typing import Callable, List
import datetime as dt


class DateRow:
    def __init__(self, cells: List[DateCell], name: str) -> None:
        self.name = name
        self.cells = cells

    def __getitem__(self, i) -> DateCell:
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

    def get_value(self, i: int) -> dt.date:
        return self.cells[i].value

    def append(self, cell: DateCell) -> None:
        self.cells.append(cell)

    @property
    def values(self) -> List[dt.date]:
        return [cell.value for cell in self.cells]

    @classmethod
    def from_values(cls, values: List, name: str, fmt: Callable = str, callback: Callable = None, locked: bool = False, validation_rules: List[Callable] = None) -> "DateRow":
        """
        Construct a row from a list of values.
        """
        cells = [DateCell(value=value, name=f"{name}[{i}]", fmt=fmt, callback=callback, locked=locked, validation_rules=validation_rules) for i, value in enumerate(values)]
        return cls(cells=cells, name=name)

    @classmethod
    def blank(cls, num_cols: int, name: str, fmt: Callable = str, callback: Callable = None, locked: bool = False, validation_rules: List[Callable] = None) -> "DateRow":
        """
        Construct a row of empty DateCells.
        """
        cells = [DateCell(value=None, name=f"{name}[{i}]", fmt=fmt, callback=callback, locked=locked, validation_rules=validation_rules) for i in range(num_cols)]
        return cls(cells=cells, name=name)
