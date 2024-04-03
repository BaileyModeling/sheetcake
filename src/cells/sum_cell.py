from .cell import Cell
from typing import List, Callable


class SumCell(Cell):
    def __init__(self, cells: List[Cell], name: str = "SumCell", tolerance = 0.0, fmt: Callable = str, callback: Callable = None, locked: bool = False, validation_rules: List[Callable] = None) -> None:
        super().__init__(value = None, name=name, tolerance=tolerance, fmt=fmt, callback=callback, locked=locked, validation_rules=validation_rules)
        self.cells = cells
        self.sum(*self.cells)
